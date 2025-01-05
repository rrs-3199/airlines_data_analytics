from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    lit,
    window,
    to_timestamp,
    avg,
    sum,
    count,
    when,
    round
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType
)
import rediscluster
import time
from datetime import datetime

# Define schema for flight data
flight_schema = StructType([
    StructField("flight_id", StringType(), True),
    StructField("airline", StringType(), True),
    StructField("aircraft_type", StringType(), True),
    StructField("departure_airport", StringType(), True),
    StructField("departure_city", StringType(), True),
    StructField("arrival_airport", StringType(), True),
    StructField("arrival_city", StringType(), True),
    StructField("scheduled_departure", StringType(), True),
    StructField("scheduled_arrival", StringType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("ticket_price", DoubleType(), True),
    StructField("flight_status", StringType(), True),
    StructField("delay_minutes", IntegerType(), True),
    StructField("route_type", StringType(), True),
    StructField("timestamp", StringType(), True)
])


class RedisHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _connect_with_cluster(self):
        return rediscluster.RedisCluster(
            startup_nodes=[{"host": self.host, "port": self.port}],
            decode_responses=True,
            skip_full_coverage_check=True
        )

    def _create_pipeline(self, connection):
        return connection.pipeline(transaction=False)

    def _execute_pipeline(self, pipeline):
        pipeline.execute()

    def write_data(self, pipeline, field, key, value):
        pipeline.hset(key, field, value)


def create_spark_session():
    return SparkSession.builder \
        .appName("FlightDataAnalytics") \
        .config("spark.streaming.stopGracefullyOnShutdown", True) \
        .getOrCreate()


def read_kafka_topic(spark, topic):
    return spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka.kafka-demo.svc.cluster.local:9092") \
        .option("subscribe", topic) \
        .option("startingOffsets", "latest") \
        .load()


def process_flight_data(east_coast_df, west_coast_df, cross_country_df):
    # Convert value column from Kafka into structured data
    def process_topic(df, route_name):
        processed_df = df.select(
            from_json(col("value").cast("string"), flight_schema).alias("data")
        ).select("data.*") \
            .withColumn("route_name", lit(route_name)) \
            .withColumn("event_time", to_timestamp(col("timestamp")))  # Convert string timestamp to timestamp type

        return processed_df

    east_coast_processed = process_topic(east_coast_df, "East Coast")
    west_coast_processed = process_topic(west_coast_df, "West Coast")
    cross_country_processed = process_topic(cross_country_df, "Cross Country")

    # Union all dataframes
    all_flights = east_coast_processed.union(west_coast_processed).union(cross_country_processed)

    # Complex analytics
    analytics_result = all_flights \
        .withWatermark("event_time", "1 minute") \
        .groupBy(
        window(col("event_time"), "5 minutes"),
        "route_name",
        "airline",
        "flight_id"
    ).agg(
        avg("ticket_price").alias("avg_ticket_price"),
        avg("delay_minutes").alias("avg_delay"),
        sum("passenger_count").alias("total_passengers"),
        count("flight_id").alias("flight_count"),
        avg(when(col("flight_status") == "Delayed", 1).otherwise(0)).alias("delay_rate")
    ) \
    .select(
        "flight_id",
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        "route_name",
        "airline",
        round("avg_ticket_price", 2).alias("avg_ticket_price"),
        round("avg_delay", 2).alias("avg_delay_minutes"),
        "total_passengers",
        "flight_count",
        round(col("delay_rate") * 100, 2).alias("delay_percentage")
    )

    return analytics_result


def write_to_redis(batch_df, batch_id):
    """
    Write batch data to Redis
    """
    if batch_df.isEmpty():
        print(f"Batch {batch_id} is empty. Skipping processing.")
        return

    start_time = time.time()
    handler = RedisHandler('canso-dplane-v1-redis.siidgk.clustercfg.use1.cache.amazonaws.com', 6379)  # Configure your Redis connection here

    try:
        connection = handler._connect_with_cluster()
        pipeline = handler._create_pipeline(connection)

        # Process in chunks
        chunk_size = 5000
        rows = batch_df.collect()
        total_rows = len(rows)

        print(f"Processing batch {batch_id} with {total_rows} rows at {datetime.now()}")

        for i in range(0, total_rows, chunk_size):
            chunk = rows[i:i + chunk_size]

            for row in chunk:
                # Create Redis key using route_name, airline and window_start
                redis_hash = f"flight_analytics:{row['route_name'].lower().replace(' ', '_')}"

                field = f"{row['flight_id']}:{row['window_start']}"

                value = f"{row['avg_ticket_price']}|{row['avg_delay_minutes']}|{row['total_passengers']}|{row['flight_count']}|{row['delay_percentage']}|{row['airline']}"

                handler.write_data(pipeline, field, redis_hash, value)


                # Store each metric as a hash field
            try:
                handler._execute_pipeline(pipeline)
                pipeline = handler._create_pipeline(connection)
            except Exception as e:
                print(f"Error executing pipeline for chunk in batch {batch_id}: {str(e)}")
                pipeline = handler._create_pipeline(connection)

        end_time = time.time()
        processing_time = end_time - start_time
        rows_per_second = total_rows / processing_time if processing_time > 0 else 0

        print(f"Batch {batch_id} processed at {datetime.now()}")
        print(f"Processed {total_rows} rows in {processing_time:.2f} seconds")
        print(f"Processing rate: {rows_per_second:.2f} rows/second")

    except Exception as e:
        print(f"Error processing batch {batch_id}: {str(e)}")
        raise
    finally:
        if 'connection' in locals():
            connection.close()


def main():
    spark = create_spark_session()

    # Read from Kafka topics
    east_coast_df = read_kafka_topic(spark, "east-coast-flights")
    west_coast_df = read_kafka_topic(spark, "west-coast-flights")
    cross_country_df = read_kafka_topic(spark, "cross-country-flights")

    # Process data and create analytics
    result_df = process_flight_data(east_coast_df, west_coast_df, cross_country_df)

    # Write results to console
    query = result_df \
        .writeStream \
        .foreachBatch(write_to_redis) \
        .outputMode("update") \
        .trigger(processingTime="30 seconds") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    main()