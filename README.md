## 🏗️ Estrutura do Projeto

O pipeline segue a **Arquitetura Medalhão**, garantindo qualidade e governança em cada etapa:

### 🥉 Camada Raw (Ingestão)
- **Origem**: Dados sintéticos gerados via biblioteca `Faker` (Python).
- **Tecnologia**: Databricks Volumes & PySpark.
- **Diferencial**: Geração dinâmica de 200k a 1MM registros por lote para teste de carga.

### 🥈 Camada Silver (Limpeza & Histórico)
- **Processamento**: Streaming incremental com **Auto Loader** (`cloudFiles`).
- **Resiliência**: Configurado com **Schema Evolution** (`addNewColumns`) e `mergeSchema`.
- **Linhagem**: Inclusão de metadados (`_metadata`) para rastreabilidade de arquivos e timestamps de modificação.
- **Histórico**: Armazenamento em formato Delta mantendo o histórico completo de alterações (Append Mode).

### 🥇 Camada Gold (Negócio & Insights)
- **Objetivo**: Tabela de `clientes_contatos_validos` pronta para consumo em BI.
- **Transformações**:
  - **Deduplicação**: Uso de `QUALIFY ROW_NUMBER()` para extrair apenas o registro mais recente por CPF.
  - **Data Quality**: Validação de formato de telefone brasileiro via Regex e exclusão de prefixos de centrais de atendimento (0800/0300).
  - **UX de Dados**: Remoção de metadados técnicos e criação de colunas amigáveis de "última atualização".

## 🛠️ Tecnologias Principais
- **Databricks Serverless** (Workflow Orchestration)
- **Unity Catalog** (Governança e Volumes)
- **Delta Lake** (Transações ACID e Schema Evolution)
- **Auto Loader** (Ingestão otimizada de arquivos)
- **Spark SQL & PySpark**
