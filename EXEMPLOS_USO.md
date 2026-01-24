# Exemplos de Uso - TOM Demand Management System

## Executável Windows: tom_demand.exe

### 1. Validar Ficheiros de Entrada

Antes de executar a priorização, valide seus ficheiros:

```cmd
tom_demand.exe validate --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv
```

### 2. Priorização Básica (Método Padrão - Sainte-Laguë)

```cmd
tom_demand.exe prioritize --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --output-dir data\output
```

### 3. Priorização com Método Específico

**Usando D'Hondt:**
```cmd
tom_demand.exe prioritize --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --method dhondt --output-dir data\output
```

**Usando WSJF:**
```cmd
tom_demand.exe prioritize --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --method wsjf --output-dir data\output
```

### 4. Executar Todos os Métodos

Executa os 3 métodos (Sainte-Laguë, D'Hondt e WSJF) e gera resultados para comparação:

```cmd
tom_demand.exe prioritize --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --all-methods --output-dir data\output
```

### 5. Priorização com Métodos Diferentes por Fila (Queue)

**WSJF para NOW, Sainte-Laguë para outras filas:**
```cmd
tom_demand.exe prioritize --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --now-method wsjf --output-dir data\output
```

**Métodos específicos para cada fila:**
```cmd
tom_demand.exe prioritize --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --now-method wsjf --next-method wsjf --later-method sainte-lague --output-dir data\output
```

### 6. Usar Configuração Personalizada

```cmd
tom_demand.exe prioritize --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --config config\custom_config.yaml --output-dir data\output
```

### 7. Comparar Todos os Métodos

Gera relatório de comparação mostrando diferenças de ranking entre métodos:

```cmd
tom_demand.exe compare --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --output data\output\comparison_report.csv --top-n 50
```

### 8. Exemplos com Caminhos Absolutos

```cmd
tom_demand.exe prioritize --ideas "C:\Projects\TOM\input\ideias.csv" --ra-weights "C:\Projects\TOM\input\weights_ra.csv" --rs-weights "C:\Projects\TOM\input\weights_rs.csv" --output-dir "C:\Projects\TOM\results"
```

### 9. Modo Interativo

Se não fornecer os parâmetros, o sistema pedirá interativamente:

```cmd
tom_demand.exe prioritize
```

O sistema perguntará:
```
Caminho para o ficheiro de IDEIAs (ideias.csv): data\input\ideias.csv
Caminho para o ficheiro de pesos RA (weights_ra.csv): data\input\weights_ra.csv
Caminho para o ficheiro de pesos RS (weights_rs.csv): data\input\weights_rs.csv
```

### 10. Ver Ajuda

**Ajuda geral:**
```cmd
tom_demand.exe --help
```

**Ajuda de comando específico:**
```cmd
tom_demand.exe prioritize --help
tom_demand.exe validate --help
tom_demand.exe compare --help
```

## Estrutura de Ficheiros Esperada

```
seu_projeto\
├── data\
│   ├── input\
│   │   ├── ideias.csv
│   │   ├── weights_ra.csv
│   │   └── weights_rs.csv
│   └── output\
│       ├── demand.csv
│       ├── demand_sainte-lague.csv
│       ├── prioritization_rs_sainte-lague.csv
│       └── metadata.json
├── config\
│   └── config.yaml
└── tom_demand.exe
```

## Ficheiros de Saída

Após a execução, encontrará em `data\output\`:

- **demand.csv** - Priorização global combinada
- **demand_[método].csv** - Priorização por método específico
- **prioritization_rs_[método].csv** - Priorização por Revenue Stream
- **metadata.json** - Metadados da execução (timestamps, parâmetros, estatísticas)

## Dicas

1. **Use aspas** se o caminho tiver espaços:
   ```cmd
   tom_demand.exe prioritize --ideas "C:\Meus Documentos\ideias.csv" ...
   ```

2. **Caminhos relativos** funcionam a partir do diretório atual:
   ```cmd
   cd C:\Users\1456253\DEV\tom_demand
   tom_demand.exe prioritize --ideas data\input\ideias.csv ...
   ```

3. **Valide sempre primeiro** para evitar erros:
   ```cmd
   tom_demand.exe validate --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv
   ```

4. **Use --all-methods** para análise comparativa:
   ```cmd
   tom_demand.exe prioritize --all-methods --ideas data\input\ideias.csv --ra-weights data\input\weights_ra.csv --rs-weights data\input\weights_rs.csv --output-dir data\output
   ```

## Formato dos Ficheiros CSV

Os ficheiros CSV devem usar **formato europeu**:
- Delimitador: ponto e vírgula (`;`)
- Separador decimal: vírgula (`,`)

**Exemplo ideias.csv:**
```csv
ID;Name;RequestingArea;RevenueStream;BudgetGroup;PriorityRA;Value;Urgency;Risk;Size
70736;WFA_Incr;PC;Corporate;APPROVAL;4;8;7;5;250
```

**Exemplo weights_ra.csv:**
```csv
RevenueStream;BudgetGroup;RequestingArea;Weight
eCommerce;Commercial;DIR_eCommerce_Commercial;30
```

**Exemplo weights_rs.csv:**
```csv
RevenueStream;Weight
eCommerce;25
Mail;20
```
