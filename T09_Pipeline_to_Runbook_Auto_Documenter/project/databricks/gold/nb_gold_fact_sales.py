# Databricks notebook source
# MAGIC %md
# MAGIC # nb_gold_fact_sales
# MAGIC Unions online and store sales into gold.fact_sales. Rebuilds the last 35 days each run (late returns).
# MAGIC NOTE: do not run a full reload: it takes ~4 hours and blocks the 06:30 SLA. Use the `days_back` widget for backfills.

# COMMAND ----------
from pyspark.sql import functions as F
load_date = dbutils.widgets.get("load_date")
days_back = int(dbutils.widgets.get("days_back") or 35)
start = F.date_sub(F.lit(load_date), days_back)
online = spark.table("silver.orders").where(F.col("order_date") >= start) \
    .select(F.col("order_date").alias("sale_date"), "customer_id", "product_sku", "qty", "amount", "channel")
store = spark.table("silver.store_sales").where(F.col("sale_date") >= start) \
    .select("sale_date", "customer_id", "product_sku", "qty", "amount", "channel")
fact = online.unionByName(store)
(fact.write.format("delta").mode("overwrite")
     .option("replaceWhere", f"sale_date >= date_sub('{load_date}', {days_back})")
     .saveAsTable("gold.fact_sales"))
