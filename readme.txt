Executar o TOM Demand

No terminal, estando já em .../ctt/tom_demand, crie (opcional) e ative um venv:
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

Instale as dependências:
pip install -r requirements.txt

Valide os ficheiros de entrada (usa os exemplos do repositório):
python3 tom_demand.py validate \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv

Execute a priorização (método padrão Sainte-Laguë) gerando saídas em data/output:
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --output-dir data/output

Outras opções úteis:
--all-methods para correr os 3 métodos;
--now-method/--next-method/--later-method para escolher métodos por fila;
config.yaml para usar outra configuração.
Resultados ficam em data/output (demand.csv, demand_[metodo].csv, etc.). Se algo falhar, partilha o erro e ajudo a corrigir.


EXECUTE
python3 tom_demand.py prioritize \
  --ideas data/input/ideias.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv
