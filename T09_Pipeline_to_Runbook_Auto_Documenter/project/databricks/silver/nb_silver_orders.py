# Databricks notebook source
# MAGIC %md
# MAGIC # nb_silver_orders
# MAGIC Merges bronze ERP orders and order lines for load_date into silver.orders (one row per order line).

# COMMAND ----------
from delta.tables import DeltaTable
from pyspark.sql import functions as F
load_date = dbutils.widgets.get("load_date")
o = spark.read.parquet(f"abfss://bronze@contosolake.dfs.core.windows.net/erp/orders/{load_date}/")
l = spark.read.parquet(f"abfss://bronze@contosolake.dfs.core.windows.net/erp/order_lines/{load_date}/")
src = (l.join(o, "order_id").select("order_id", "line_no", "order_date", "customer_id", "product_sku", "qty", "amount", "status")
        .withColumn("channel", F.lit("online")))
(DeltaTable.forName(spark, "silver.orders").alias("t")
   .merge(src.alias("s"), "t.order_id = s.order_id AND t.line_no = s.line_no")
   .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())
