import asyncio
import httpx
import xml.etree.ElementTree as ET

urls = [
    ("Art 14 TRLGSS", "BOE-A-2015-11724", "a14"),
    ("Art 167 TRLGSS (IT pago)", "BOE-A-2015-11724", "a167"),
    ("Art 169 TRLGSS (IT pago)", "BOE-A-2015-11724", "a169"),
    ("Art 173 TRLGSS (Menstruacion)", "BOE-A-2015-11724", "a173"),
    ("Art 196 TRLGSS (IPT alzado)", "BOE-A-2015-11724", "a196"),
    ("Art 31 TRLGSS (Intereses)", "BOE-A-2015-11724", "a31"),
    ("Art 248 TRLGSS (Tiempo Parcial)", "BOE-A-2015-11724", "a248"),
    ("Art 237 TRLGSS (Excedencia)", "BOE-A-2015-11724", "a237"),
]

async def fetch_article(name, law_id, block):
    url = f"https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{law_id}/texto/bloque/{block}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"Accept": "application/xml"})
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            # Find the most recent version
            version = root.find(".//version")
            if version is not None:
                texts = [p.text for p in version.findall(".//p") if p.text]
                return name, "\n".join(texts)
        return name, f"Error {resp.status_code}"

async def main():
    tasks = [fetch_article(n, l, b) for n, l, b in urls]
    results = await asyncio.gather(*tasks)
    with open("articulos_boe.md", "w") as f:
        for name, text in results:
            f.write(f"### {name}\n{text}\n\n")

asyncio.run(main())
