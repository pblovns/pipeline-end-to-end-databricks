import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """Create a Spark session for testing"""
    return (
        SparkSession.builder
        .appName("pytest-spark")
        .master("local[1]")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .getOrCreate()
    )


@pytest.fixture(scope="function")
def spark_context(spark):
    """Provide clean Spark session for each test"""
    yield spark
    spark.sql("CLEAR CACHE")
