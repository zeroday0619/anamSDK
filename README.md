# Korea University Anam Hospital internal API for Python SDK
KUMC Internel API for Python SDK


## Usage

### Example code
```python
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
```

## **Disclaimer**
This project has been developed for research purposes and the creators are not responsible for anything that happens as a result of using this project. We would also like to inform you that the project may be taken down at any time by the demands of KUMC.

## **License**
Licensed under the [LGPL-2.1](./LICENSE)