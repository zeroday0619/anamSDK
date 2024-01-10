import json
import asyncio
from kumc import KUMCClient

async def main():
    app = KUMCClient()

    await app.sign_in()
    resp = await app.get_hospitalization_and_discharge_history(hpCd="AA", inqrStrtYmd=20220130)
    print(
        json.dumps(
            resp, 
            indent=4, 
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    asyncio.run(main())