# Databricks notebook source
# MAGIC %md
# MAGIC # nb_gold_customer_360
# MAGIC Customer 360 table used by the Power BI "Retail Sales" model (Customer 360 page).

# COMMAND ----------
from pyspark.sql import functions as F
f = spark.table("gold.fact_sales")
c = spark.table("silver.customers")
kpi = f.groupBy("customer_id").agg(F.sum("amount").alias("lifetime_value"), F.max("sale_date").alias("last_purchase"),
                                   F.countDistinct("channel").alias("channels_used"))
c360 = c.join(kpi, "customer_id", "left").select("customer_id", "full_name", "email", "phone", "city", "segment",
                                                  "lifetime_value", "last_purchase", "channels_used")
c360.write.format("delta").mode("overwrite").saveAsTable("gold.customer_360")
