import asyncio
import httpx
import xml.etree.ElementTree as ET

async def fetch_article():
    url = f"https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2015-11724/texto/bloque/a173"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"Accept": "application/xml"})
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            version = root.find(".//version")
            if version is not None:
                texts = [p.text for p in version.findall(".//p") if p.text]
                print("\n".join(texts))
        else:
            print(f"Error {resp.status_code}")

asyncio.run(fetch_article())
