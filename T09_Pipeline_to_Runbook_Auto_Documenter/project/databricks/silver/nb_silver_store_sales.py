# Databricks notebook source
# MAGIC %md
# MAGIC # nb_silver_store_sales
# MAGIC Cleans bronze.store_sales for load_date into silver.store_sales; maps loyalty cards to customers.

# COMMAND ----------
from pyspark.sql import functions as F
load_date = dbutils.widgets.get("load_date")
s = spark.table("bronze.store_sales").where(F.col("_load_date") == load_date)
cust = spark.table("silver.customers").select("customer_id", "loyalty_card_no")
silver = (s.join(cust, "loyalty_card_no", "left")
           .select("store_id", "sale_date", "receipt_no", "product_sku", "qty", "amount", "customer_id")
           .withColumn("channel", F.lit("store")))
silver.write.format("delta").mode("overwrite").option("replaceWhere", f"sale_date = '{load_date}'").saveAsTable("silver.store_sales")
