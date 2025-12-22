# 🚀 Pipeline de Dados End-to-End com Databricks

Este repositório contém o desenvolvimento de um pipeline de dados completo utilizando a **Arquitetura Medalhão**, processado integralmente no **Databricks** e governado pelo **Unity Catalog**.

## 🏗️ Visão Geral da Arquitetura
O projeto simula um cenário real de ingestão e processamento de dados de clientes, dividindo-se em três etapas principais: Raw (Bronze), Silver e Gold.

### 🥉 Camada Raw (Ingestão) - [CONCLUÍDA]
Nesta etapa, o foco foi garantir que os dados "aterrizassem" no ambiente de nuvem de forma íntegra e organizada.

**Destaques Técnicos:**
- **Geração de Dados Sintéticos**: Uso da biblioteca `Faker` (localidade `pt_BR`) para criar 10.000 registros realistas (Nome, CPF, Endereço, etc).
- **Processamento Distribuído**: Implementação via **PySpark** para conversão de listas Python em DataFrames escaláveis.
- **Governança de Tempo**: Ajuste preciso de timezone (`America/Sao_Paulo`) usando `zoneinfo` para garantir rastreabilidade real dos logs.
- **Data Cleaning Preventivo**: Tratamento de quebras de linha em endereços para evitar corrupção estrutural no formato CSV.
- **Armazenamento**: Escrita em **Databricks Volumes** com particionamento dinâmico por data/hora.

## 🛠️ Tecnologias e Ferramentas
- **Linguagem**: Python & PySpark
- **Ambiente**: Databricks (Community Edition)
- **Governança**: Unity Catalog (Volumes)
- **DevOps**: Integração Git nativa (Git Folders) e Gerenciamento de dependências via `requirements.txt`.
- **Orquestração**: Databricks Workflows (Jobs) agendados.

## 🚀 Como Executar
1. Configure o repositório no seu Databricks via **Git Folders**.
2. Crie um **Job** no Databricks Workflows.
3. Adicione a biblioteca `faker` nas dependências do Job (via PyPI ou `requirements.txt`).
4. Agende ou execute manualmente o notebook `input_fake_data_raw`.

## 🔜 Próximos Passos
- [ ] **Camada Silver**: Leitura incremental (Auto Loader), tipagem estrita de dados e conversão para formato **Delta**.
- [ ] **Camada Gold**: Criação de agregações de negócio e tabelas prontas para consumo em BI.
