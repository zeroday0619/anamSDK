import os
from datetime import datetime
from httpx import AsyncClient
from src.auth import Login
from src.utils import get_now_yymmdd

class AnamClient(Login):
    def __init__(self, session: AsyncClient) -> None:
        super().__init__(
            session=session,
            username=os.environ.get("ANAM_USERNAME"),
            password=os.environ.get("ANAM_PASSWORD")
        )
        self.anam_api_url = "https://anam.kumc.or.kr/api"
        self.is_sign_in_executed = False
    
    def raise_for_sign_in(self):
        if not self.is_sign_in_executed:
            raise NotImplementedError("Preceding function `sign_in` must be executed first")
    
    async def sign_in(self):
        await super().sign_in()
        self.is_sign_in_executed = True

    async def get_info(self) -> dict:
        self.raise_for_sign_in()
        
        raw_response = await self.session.get(self.anam_api_url+"/info.do")
        response = raw_response.raise_for_status()
        result = self.serialization(response)            
        return result

    async def get_reservations(self, hpCd: str = "AA", apstYmd: int = get_now_yymmdd(), apfnYmd: int | None = None) -> list:
        if not apfnYmd:
            raise ValueError("`apfnYmd` must be specified")

        self.raise_for_sign_in()

        raw_response = await self.session.get(
            self.anam_api_url+"/mypage/reservation/list.do",
            params={
                "hpCd": hpCd,
                "apstYmd": apstYmd,
                "apfnYmd": apfnYmd
            }
        )
        response = raw_response.raise_for_status()
        result = self.serialization(response)['list']
        return result
    
    async def get_health_check_result(self, hpCd: str = "AA", strtYmd: int = get_now_yymmdd(), fnshYmd: int | None = None) -> dict:
        if not fnshYmd:
            raise ValueError("`fnshYmd` must be specified")
        
        self.raise_for_sign_in()
        
        raw_response = await self.session.get(
            self.anam_api_url+"/healthCheckResult.do",
            params={
                "hpCd": hpCd,
                "strtYmd": strtYmd,
                "fnshYmd": fnshYmd    
            }
        )
        response = raw_response.raise_for_status()
        result = self.serialization(response)
        return result
    
    async def get_medication_prescription_history(self, hpCd: str = "AA", ordrYmd1: int = None, ordrYmd2: int = None):
        if not (ordrYmd1 and ordrYmd2):
            raise ValueError("`ordrYmd1` and `ordrYmd2` must be specified")

        self.raise_for_sign_in()

        raw_response = await self.session.get(
            self.anam_api_url+"/drugList.do",
            params={
                "hpCd": hpCd,
                "ordrYmd1": ordrYmd1,
                "ordrYmd2": ordrYmd2
            }
        )
        response = raw_response.raise_for_status()
        result = self.serialization(response)
        return result
        
        