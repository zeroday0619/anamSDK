import json
import asyncio
from httpx import AsyncClient
from src.client import AnamClient
from fake_useragent import UserAgent

async def main():
    async with AsyncClient(
        headers={
            "User-Agent": UserAgent().random
        }
    ) as session:
        app = AnamClient(session=session)
        await app.sign_in()
        resp = await app.get_medication_prescription_history(ordrYmd1=20231111, ordrYmd2=20231230)
        print(json.dumps(resp, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())