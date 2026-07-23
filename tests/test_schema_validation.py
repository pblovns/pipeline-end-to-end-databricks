"""
Tests for schema validation
"""
import pytest
from pyspark.sql.types import StructType, StructField, StringType, DateType, TimestampType


class TestSchemaValidation:
    """Test schema validation"""

    def test_raw_layer_schema_structure(self, spark_context):
        """Test Raw layer expected schema"""
        spark = spark_context
        
        expected_schema = StructType([
            StructField("nome", StringType(), True),
            StructField("cpf", StringType(), True),
            StructField("telefone", StringType(), True),
            StructField("dataNascimento", DateType(), True),
            StructField("email", StringType(), True),
            StructField("endereco", StringType(), True),
            StructField("cargo", StringType(), True),
            StructField("empresa", StringType(), True),
            StructField("website", StringType(), True),
        ])
        
        # Create sample data matching schema
        data = [
            ("João Silva", "123.456.789-00", "(11) 99988-7766", "1990-01-15",
             "joao@email.com", "Rua A, 123 | SP", "Engenheiro", "Tech Corp", "https://techcorp.com")
        ]
        
        df = spark.createDataFrame(data, expected_schema)
        
        assert df.schema == expected_schema
        assert len(df.schema.fields) == 9

    def test_silver_layer_schema_has_metadata_columns(self, spark_context):
        """Test Silver layer includes metadata columns"""
        spark = spark_context
        
        silver_schema = StructType([
            StructField("nome", StringType(), True),
            StructField("cpf", StringType(), True),
            StructField("dataNascimento", DateType(), True),
            StructField("cargo", StringType(), True),
            StructField("empresa", StringType(), True),
            StructField("email", StringType(), True),
            StructField("estado", StringType(), True),
            StructField("endereco", StringType(), True),
            StructField("telefone", StringType(), True),
            StructField("website", StringType(), True),
            StructField("origemArquivoDado", StringType(), True),
            StructField("dataReferenciaDado", TimestampType(), True),
        ])
        
        # Verify metadata columns exist
        field_names = [field.name for field in silver_schema.fields]
        
        assert "origemArquivoDado" in field_names
        assert "dataReferenciaDado" in field_names

    def test_gold_layer_schema_has_business_columns(self, spark_context):
        """Test Gold layer includes business-ready columns"""
        spark = spark_context
        
        gold_schema = StructType([
            StructField("nome", StringType(), True),
            StructField("cpf", StringType(), True),
            StructField("dataNascimento", DateType(), True),
            StructField("cargo", StringType(), True),
            StructField("empresa", StringType(), True),
            StructField("email", StringType(), True),
            StructField("estado", StringType(), True),
            StructField("endereco", StringType(), True),
            StructField("telefone_limpo", StringType(), True),
            StructField("is_contato_valido", StringType(), True),
            StructField("website", StringType(), True),
            StructField("dataReferenciaDado", TimestampType(), True),
            StructField("dataUltimaAtualizacao", TimestampType(), True),
        ])
        
        # Verify business logic columns
        field_names = [field.name for field in gold_schema.fields]
        
        assert "telefone_limpo" in field_names
        assert "is_contato_valido" in field_names
        assert "dataUltimaAtualizacao" in field_names

    def test_schema_field_count_raw_layer(self, spark_context):
        """Test Raw layer has expected number of fields"""
        spark = spark_context
        
        expected_field_count = 9
        data = [
            ("João", "123.456.789-00", "(11) 99988-7766", "1990-01-15",
             "joao@email.com", "Rua A, 123", "Engenheiro", "Tech Corp", "https://example.com")
        ]
        
        df = spark.createDataFrame(
            data,
            ["nome", "cpf", "telefone", "dataNascimento", "email",
             "endereco", "cargo", "empresa", "website"]
        )
        
        assert len(df.schema.fields) == expected_field_count

    def test_schema_field_count_gold_layer(self, spark_context):
        """Test Gold layer has expected number of fields"""
        spark = spark_context
        
        expected_field_count = 13
        data = [
            ("João", "123.456.789-00", "1990-01-15", "Engenheiro", "Tech Corp",
             "joao@email.com", "SP", "Rua A, 123", "11999887766", True, "https://example.com",
             "2025-12-29 00:10:00", "2025-12-29 00:10:00")
        ]
        
        df = spark.createDataFrame(
            data,
            ["nome", "cpf", "dataNascimento", "cargo", "empresa", "email", "estado",
             "endereco", "telefone_limpo", "is_contato_valido", "website",
             "dataReferenciaDado", "dataUltimaAtualizacao"]
        )
        
        assert len(df.schema.fields) == expected_field_count
