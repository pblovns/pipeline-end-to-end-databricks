# 🧪 Testes Unitários - Pipeline Databricks

Documentação completa sobre a estratégia de testes do projeto.

## 📋 Visão Geral

Este projeto implementa testes unitários para validar:
- **Geração de dados** (Faker)
- **Validação e limpeza** de dados
- **Schema e estrutura** dos DataFrames
- **Transformações** PySpark

## 🚀 Começando

### Instalação

```bash
# Instalar dependências de teste
pip install -r requirements-test.txt
```

### Executar Testes

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=. --cov-report=html

# Executar testes de um arquivo específico
pytest tests/test_data_generation.py -v

# Executar testes com marcadores
pytest -m unit -v
```

## 📁 Estrutura de Testes

```
tests/
├── __init__.py                  # Inicialização do módulo
├── conftest.py                  # Configurações e fixtures do pytest
├── test_data_generation.py      # Testes de geração de dados (Raw)
├── test_data_validation.py      # Testes de validação e transformação
└── test_schema_validation.py    # Testes de schema dos DataFrames
```

## 🧩 Módulos de Teste

### 1. **test_data_generation.py**
Valida a configuração do Faker e geração de dados:
- ✅ Locale pt_BR disponível
- ✅ CPF gerado com formato válido
- ✅ Email contém @ e .
- ✅ Perfil contém todos os campos obrigatórios
- ✅ Múltiplos perfis são únicos

**Caso de Uso**: Garantir que dados fake são gerados corretamente

### 2. **test_data_validation.py**
Testa validação e transformações de dados:
- ✅ Limpeza de CPF (remove . e -)
- ✅ Regex de telefone válido
- ✅ Rejeição de centrais de atendimento (0800, 0300, etc)
- ✅ Validação de nulidade em Spark
- ✅ Contagem de registros

**Caso de Uso**: Validar transformações de cada camada (Raw → Silver → Gold)

### 3. **test_schema_validation.py**
Valida estrutura dos DataFrames:
- ✅ Schema da camada Raw
- ✅ Schema da camada Silver (com metadados)
- ✅ Schema da camada Gold (com colunas de negócio)
- ✅ Contagem de colunas esperadas

**Caso de Uso**: Detectar mudanças inesperadas no schema

## 🔧 Fixtures

### `spark_context`
Fornece uma sessão Spark limpa para cada teste.

```python
def test_exemplo(spark_context):
    df = spark_context.createDataFrame(...)
    assert df.count() > 0
```

## 📊 Cobertura de Testes

Atualmente cobrindo:
- **Geração de Dados**: 6 testes
- **Validação de Dados**: 5 testes
- **Schema**: 5 testes
- **Total**: 16 testes

## 🎯 Próximos Passos

- [ ] Testes de integração com Databricks
- [ ] Testes de performance/volume
- [ ] Validação com Great Expectations
- [ ] CI/CD pipeline com GitHub Actions

## 📝 Exemplo de Novo Teste

```python
import pytest
from pyspark.sql.functions import col

def test_my_transformation(spark_context):
    """Descrever o que o teste valida"""
    # Arrange: preparar dados
    data = [("João",), ("Maria",)]
    df = spark_context.createDataFrame(data, ["nome"])
    
    # Act: executar transformação
    df_result = df.filter(col("nome") == "João")
    
    # Assert: validar resultado
    assert df_result.count() == 1
    assert df_result.collect()[0]["nome"] == "João"
```

## 🔍 Troubleshooting

### Erro: "Spark Session não inicializado"
**Solução**: Use a fixture `spark_context` em seus testes.

### Erro: "Module not found: pyspark"
**Solução**: Execute `pip install -r requirements-test.txt`

### Erro: "Permissão negada" ao executar pytest
**Solução**: Use `chmod +x pytest` ou execute via Python: `python -m pytest`

## 📚 Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [PySpark Testing](https://spark.apache.org/docs/latest/api/python/index.html)
- [Great Expectations](https://greatexpectations.io/)
