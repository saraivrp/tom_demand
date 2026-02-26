Executar o TOM Demand

#QUICK APPROACH
python3 tom_demand.py prioritize \
  --ideas data/input/ideas20260224.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --next-method wsjf \
  --later-method sainte-lague

python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602_25.csv \
  --ra-weights data/input/weights_ra_25.csv \
  --rs-weights data/input/weights_rs_25.csv \
  --next-method wsjf \
  --later-method sainte-lague


#DETAIL


No terminal, estando já em .../ctt/tom_demand, crie (opcional) e ative um venv:
python3 -m venv .venv source .venv/bin/activate   # Windows: .venv\Scripts\activate

Instale as dependências:
pip install -r requirements.txt

Valide os ficheiros de entrada (usa os exemplos do repositório):
python3 tom_demand.py validate \
  --ideas data/input/ideas.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv

Execute a priorização (método padrão Sainte-Laguë) gerando saídas em data/output:
python3 tom_demand.py prioritize \
  --ideas data/input/ideas.csv \
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
  --ideas data/input/ideas.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv


EXECUTE DETAIL
python3 tom_demand.py prioritize \
  --ideas data/input/ideas202602.csv \
  --ra-weights data/input/weights_ra.csv \
  --rs-weights data/input/weights_rs.csv \
  --next-method wsjf \
  --later-method sainte-lague


  #####################
  RUNNING FRONTEND

Backend (API):

# from project root
pip install -r requirements.txt
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
API docs: http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8000/api/v1/health
Frontend (Expo React Native Web):

# from project root
cd frontend
npm install
npm run web
Web app opens on Expo’s URL (usually http://localhost:19006).
If auth is enabled on backend:

# backend
export AUTH_ENABLED=true
export API_KEY=change-me
uvicorn src.api.main:app --reload
# frontend (new terminal)
cd frontend
export EXPO_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
export EXPO_PUBLIC_API_KEY=change-me
export EXPO_PUBLIC_API_ROLE=executor
npm run web
Alternative (run both with Docker):

docker compose up --build
API: http://localhost:8000
Frontend: http://localhost:19006


#######################
TEST APIs
{
  "ideas_path": "data/input/ideas202602.csv",
  "ra_weights_path": "data/input/weights_ra.csv",
  "rs_weights_path": "data/input/weights_rs.csv",
  "config_path": "config/config.yaml"
}
