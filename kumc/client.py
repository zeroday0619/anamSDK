import os
from httpx import AsyncClient
from .auth import Login
from .utils import get_now_yymmdd


class AnamClient(Login):
    def __init__(self, session: AsyncClient, username: str | None = None, password: str | None = None) -> None:

        # Do not hardcode username and password
        if username or password:
            super().__init__(
                session=session,
                username=username,
                password=password
            )
        else:
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
    
    async def get_ambulatory_care_history(self, hpCd: str = "AA", inqrStrtYmd: int = None, inqrFnshYmd: int = get_now_yymmdd(), inqrDvsnCd: int = 2):
        if not (inqrStrtYmd and inqrFnshYmd):
            raise ValueError("`inqrStrtYmd` and `inqrFnshYmd` must be specified")

        self.raise_for_sign_in()

        raw_response = await self.session.get(
            self.anam_api_url+"/schedule.do",
            params={
                "hpCd": hpCd,
                "inqrStrtYmd": inqrStrtYmd,
                "inqrFnshYmd": inqrFnshYmd,
                "inqrDvsnCd": inqrDvsnCd
            }
        )
        response = raw_response.raise_for_status()
        result = self.serialization(response).get('list')
        return result
        
    async def get_hospitalization_and_discharge_history(self, hpCd: str = "AA", inqrStrtYmd: int = None, inqrFnshYmd: int = get_now_yymmdd(), inqrDvsnCd: int = 3):
        result = await self.get_ambulatory_care_history(
            hpCd=hpCd,
            inqrStrtYmd=inqrStrtYmd,
            inqrFnshYmd=inqrFnshYmd,
            inqrDvsnCd=inqrDvsnCd
        )
        return result
    
    async def get_payed_list(self, hpCd: str = "AA", strtYmd: int = None, fnshYmd: int = get_now_yymmdd(), codvCd: str = "O"):
        self.raise_for_sign_in()

        if not strtYmd:
            raise ValueError("`strtYmd` must be specified")

        raw_response = await self.session.post(
            self.anam_api_url+"/payCompleteList.do",
            params={
                "hpCd": hpCd,
                "strtYmd": strtYmd,
                "fnshYmd": fnshYmd,
                "codvCd": codvCd
            }
        )
        response = raw_response.raise_for_status()
        result = self.serialization(response).get('acaRealInsrClamMdrpOutDVOList')
        return result
    
    async def get_payed_detail(self, hpCd: str = "AA", mdrpNo: int = None):
        self.raise_for_sign_in()

        if not mdrpNo:
            raise ValueError("`mdrpNo` must be specified")

        raw_response = await self.session.post(
            self.anam_api_url+"/payCompleteyDetail.do",
            params={
                "hpCd": hpCd,
                "mdrpNo": mdrpNo
            }
        )
        print(raw_response.status_code)
        response = raw_response.raise_for_status()
        result = self.serialization(response)
        return result
