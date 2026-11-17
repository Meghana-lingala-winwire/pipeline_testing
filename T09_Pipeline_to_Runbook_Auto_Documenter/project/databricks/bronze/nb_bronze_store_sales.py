# Databricks notebook source
# MAGIC %md
# MAGIC # nb_bronze_store_sales
# MAGIC Loads the store POS file from landing into bronze.store_sales. Idempotent per load_date (replaceWhere).

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType, DateType
load_date = dbutils.widgets.get("load_date")
schema = StructType([StructField("store_id", StringType()), StructField("sale_date", DateType()), StructField("receipt_no", StringType()),
                     StructField("product_sku", StringType()), StructField("qty", IntegerType()), StructField("amount", DecimalType(18, 2)),
                     StructField("loyalty_card_no", StringType()), StructField("customer_phone", StringType())])
df = (spark.read.schema(schema).option("header", "true").csv(f"abfss://landing@contosolake.dfs.core.windows.net/stores/{load_date}/")
        .withColumn("_load_date", F.lit(load_date)))
df.write.format("delta").mode("overwrite").option("replaceWhere", f"_load_date = '{load_date}'").saveAsTable("bronze.store_sales")
