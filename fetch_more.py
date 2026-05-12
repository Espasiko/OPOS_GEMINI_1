import asyncio
import httpx
import xml.etree.ElementTree as ET

urls = [
    ("Art 15 TRLGSS (Resp solidaria/subsidiaria)", "a15"),
    ("Art 31 TRLGSS (Intereses)", "a31"),
    ("Art 352 TRLGSS (Prest flia asig)", "a352"),
    ("Art 353 TRLGSS (Parto multiple)", "a353"),
    ("Art 322 TRLGSS (Lagunas RETA)", "a322"),
    ("Art 178 TRLGSS (Menstruacion IT)", "a178"),
    ("Art 214 TRLGSS (Jubilacion activa)", "a214"),
    ("Art 173 TRLGSS", "a173"),
    ("Art 169 TRLGSS", "a169"),
]

async def fetch_article(name, block):
    url = f"https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2015-11724/texto/bloque/{block}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"Accept": "application/xml"})
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            version = root.find(".//version")
            if version is not None:
                # keep html tags like bold etc stripped by using pure itertext
                text = "".join(version.itertext())
                # reduce multiple newlines
                import re
                text = re.sub(r'\n\s*\n', '\n', text)
                return name, text
        return name, f"Error {resp.status_code}"

async def main():
    tasks = [fetch_article(n, b) for n, b in urls]
    results = await asyncio.gather(*tasks)
    with open("articulos_more.md", "w") as f:
        for name, text in results:
            f.write(f"### {name}\n{text}\n\n")

asyncio.run(main())
