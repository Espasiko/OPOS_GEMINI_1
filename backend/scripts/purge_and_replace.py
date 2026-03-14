import json

basura = [
    "BOE-A-1982-9050", "BOE-A-1985-22915", "BOE-A-1988-9526", "BOE-A-1995-2081",
    "BOE-A-1995-24156", "BOE-A-2001-20795", "BOE-A-2006-16891", "BOE-A-2006-19348",
    "BOE-A-2008-17156", "BOE-A-2009-3780", "BOE-A-2009-5693", "BOE-A-2020-6898",
    "BOE-A-2022-7260", "BOE-A-2023-25411", 
    "BOE-A-2023-6945", "BOE-A-2011-15673", "BOE-A-2020-2047", "BOE-A-1995-10652",
    "BOE-A-1995-10653", "BOE-A-2010-1172"
]

reemplazos = {
    "RDL 2/2023 (Pensiones)": "BOE-A-2023-6967",
    "Ley 36/2011 (Jurisdicción Social)": "BOE-A-2011-15936",
    "RD 139/2020 (Estructura Orgánica AGE)": "BOE-A-2020-1246",
    "RD 364/1995 (Ingreso Personal Administración)": "BOE-A-1995-8729",
    "RD 365/1995 (Situaciones Administrativas)": "BOE-A-1995-8730",
    "RD 4/2010 (Esquema Nacional Interoperabilidad)": "BOE-A-2010-1331"
}
print(json.dumps(basura))
