import json
import urllib.request

falsas = [
  'Se presume relación laboral quien presta servicios por cuenta ajena, SALVO prueba en contrario (presunción iuris tantum).',
  'Contrato formativo: el tiempo de trabajo no puede superar el límite legal, SALVO que el trabajador sea contratado a tiempo parcial.',
  'Periodo de prueba máximo: 6 meses técnicos, 2 meses resto, SALVO lo que disponga el Convenio Colectivo.',
  'Las horas extra NO computan para la base de contingencias comunes, SALVO para cotizar por accidentes de trabajo y enf. profesionales.',
  'El alta médica extingue la IT el mismo día, SALVO que el trabajador estuviera en víspera de festivo (efectos al día siguiente hábil).',
  'Las infracciones prescriben a los 3 años en lo social, SALVO las de Seguridad Social que prescriben a los 4 años.',
  'El recurso contra un acta de infracción sirve para la liquidación conjunta, SALVO manifestación en contrario.',
  'Los hechos constatados por el Inspector tienen presunción de certeza iuris tantum (SALVO prueba en contrario).',
  'El impago de la sanción en plazo inicia el apremio, SALVO que se garantice el importe con aval bancario.'
]

cypher = 'MATCH ()-[r:EXCEPCION_A]->() WHERE r.descripcion IN $falsas DELETE r'

payload = {'statements': [{'statement': cypher, 'parameters': {'falsas': falsas}}]}

req = urllib.request.Request('http://localhost:7474/db/neo4j/tx/commit', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'Authorization': 'Basic bmVvNGo6b3Bvc2l0YWlhMjAyNg=='})

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        res = json.loads(response.read().decode('utf-8'))
        if res.get('errors'):
            print(f'Error Neo4j: {res["errors"]}')
        else:
            print('Basura borrada correctamente.')
except Exception as e:
    print(f'Excepción HTTP: {e}')
