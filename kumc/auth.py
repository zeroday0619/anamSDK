from typing import TypeVar
from httpx import Response
from httpx import AsyncClient
from base64 import b64encode
from .exception import LoginError


AsyncClientT = TypeVar("AsyncClientT", bound=AsyncClient)

class Login:
    def __init__(self, session: AsyncClient, username: str, password: str):
        self.login_url = "https://anam.kumc.or.kr/member/login.do"

        if not username or not password:
            raise LoginError("Username and password are required")
        
        self.username = username
        self.password = password
        self.enc_password = b64encode(
            password.encode("utf-8")
        ).decode("utf-8")
        self.session = session

        self.payload = {
            "memId": self.username,
            "memPwd": self.password,
            "memPwEnc": self.enc_password
        }
    
    @staticmethod
    def serialization(response: Response) -> dict:
        return response.json()
    
    async def sign_in(self) -> AsyncClientT:
        raw_response = await self.session.post(self.login_url, data=self.payload)
        response = raw_response.raise_for_status()
        result = self.serialization(response)['result']
        if result["status"] and result['code'] == 'OK':
            self.session.cookies.update(response.cookies)
            return self.session
        else:
            error_type = result['code']
            error_message = result['message']
            message = f"{error_type}: {error_message}"
            raise LoginError(message)
