"""
Tests for data validation and transformations
"""
import pytest
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace


class TestDataValidation:
    """Test data validation functions"""

    def test_cpf_cleaning_removes_special_chars(self):
        """Test CPF cleaning removes dots and dashes"""
        cpf_with_chars = "123.456.789-00"
        cpf_clean = cpf_with_chars.replace(".", "").replace("-", "")
        
        assert cpf_clean == "12345678900"
        assert "." not in cpf_clean
        assert "-" not in cpf_clean

    def test_phone_regex_valid_numbers(self):
        """Test regex for valid Brazilian phone numbers"""
        pattern = r'^[1-9][1-9]9[0-9]{8}$'
        
        # Valid numbers
        valid_phones = [
            "11999887766",  # São Paulo mobile
            "21987654321",  # Rio mobile
            "85988776655",  # Ceará mobile
        ]
        
        for phone in valid_phones:
            assert re.match(pattern, phone), f"Phone {phone} should be valid"

    def test_phone_regex_invalid_numbers(self):
        """Test regex rejects invalid Brazilian phone numbers"""
        pattern = r'^[1-9][1-9]9[0-9]{8}$'
        
        # Invalid numbers
        invalid_phones = [
            "08001234567",  # Central de atendimento 0800
            "03001234567",  # Central de atendimento 0300
            "05001234567",  # Central de atendimento 0500
            "09001234567",  # Central de atendimento 0900
            "1199988",      # Too short
            "119998876661", # Too long
            "01999887766",  # Starts with 0
        ]
        
        for phone in invalid_phones:
            assert not re.match(pattern, phone), f"Phone {phone} should be invalid"

    def test_phone_prefix_exclusion(self):
        """Test exclusion of service center prefixes"""
        invalid_prefixes = ['0300', '0500', '0800', '0900']
        test_numbers = ["03001234567", "05001234567", "08001234567", "09001234567"]
        
        for number in test_numbers:
            prefix = number[:4]
            assert prefix in invalid_prefixes


class TestSparkTransformations:
    """Test Spark DataFrame transformations"""

    def test_cpf_cleaning_in_spark(self, spark_context):
        """Test CPF cleaning transformation in Spark"""
        spark = spark_context
        
        data = [
            ("123.456.789-00",),
            ("111.222.333-44",),
            ("999.888.777-66",),
        ]
        
        df = spark.createDataFrame(data, ["cpf"])
        df_clean = df.withColumn("cpf_clean", regexp_replace(col("cpf"), "[. -]", ""))
        
        result = df_clean.collect()
        
        assert result[0]["cpf_clean"] == "12345678900"
        assert result[1]["cpf_clean"] == "11122233344"
        assert result[2]["cpf_clean"] == "99988877766"

    def test_phone_cleaning_in_spark(self, spark_context):
        """Test phone number cleaning in Spark"""
        spark = spark_context
        
        data = [
            ("(11) 99988-7766",),
            ("(21) 98765-4321",),
            ("+55 85 98877-6655",),
        ]
        
        df = spark.createDataFrame(data, ["telefone"])
        df_clean = df.withColumn("telefone_clean", regexp_replace(col("telefone"), "[+ ( ) -]", ""))
        
        result = df_clean.collect()
        
        assert result[0]["telefone_clean"] == "11999887766"
        assert result[1]["telefone_clean"] == "21987654321"
        assert result[2]["telefone_clean"] == "5585988776655"

    def test_dataframe_not_null_validation(self, spark_context):
        """Test validation of non-null columns"""
        spark = spark_context
        
        data = [
            ("João", "123.456.789-00", "joao@email.com"),
            ("Maria", "111.222.333-44", "maria@email.com"),
            ("Pedro", "999.888.777-66", None),  # Invalid: null email
        ]
        
        df = spark.createDataFrame(data, ["nome", "cpf", "email"])
        
        # Count non-null emails
        non_null_count = df.filter(col("email").isNotNull()).count()
        assert non_null_count == 2
        
        # Count null emails
        null_count = df.filter(col("email").isNull()).count()
        assert null_count == 1

    def test_dataframe_row_count(self, spark_context):
        """Test row counting in Spark DataFrame"""
        spark = spark_context
        
        data = [(f"cliente_{i}",) for i in range(100)]
        df = spark.createDataFrame(data, ["nome"])
        
        assert df.count() == 100
