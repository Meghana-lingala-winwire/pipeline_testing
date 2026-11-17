# Databricks notebook source
# MAGIC %md
# MAGIC # nb_silver_customers
# MAGIC Builds silver.customers from bronze ERP customers (parquet). Full rebuild each run.

# COMMAND ----------
from pyspark.sql import functions as F
c = spark.read.parquet("abfss://bronze@contosolake.dfs.core.windows.net/erp/customers/")
silver = (c.select("customer_id", "full_name", "email", "phone", "city", "postcode", "segment", "loyalty_card_no")
           .withColumn("email", F.lower("email")).dropDuplicates(["customer_id"]))
silver.write.format("delta").mode("overwrite").saveAsTable("silver.customers")
