# ✈️ **Airlines Data Analytics**

## 📄 **Project Overview**  
Apache Kafka is an open-source distributed event streaming platform designed for **high-throughput**, **fault-tolerant**, and **real-time** data streaming.For my project, I am developing a PySpark streaming application that processes data from a streaming source.Kafka was chosen as the streaming source due to the following reasons:

**Scalability:** Kafka can handle high volumes of data with ease, allowing my application to scale as data increases.

**Fault Tolerance:** Kafka’s distributed architecture ensures that data remains available even in case of node failures.

**High Throughput:** Kafka is designed to handle large amounts of data in real-time, ensuring efficient streaming for PySpark applications.

**Compatibility:** Kafka integrates seamlessly with PySpark, providing robust support for processing and analyzing streaming data.

**Flexibility:** With Kafka topics, I can segregate data streams logically, enabling better management and processing of incoming data.




##  **Data Source**  
I have created three Kafka topics to handle different streams of data. These topics represent distinct regions and use cases, ensuring that data from different sources is logically separated and processed independently:

**East Coast:** This topic is designated for streaming data originating from the East Coast region.

**West Coast:** This topic handles data streams from the West Coast region.

**Cross Country:** This topic is used for data that spans or connects across multiple regions, enabling analysis of nationwide trends.



### 🏗 **Architecture**  

### 🔄 **Data Transform**  

This PySpark application is designed to process flight data from Kafka topics in real-time, perform analytics, and write the results to a Redis cluster for further consumption. Below is an explanation of the key components of the streaming job:

**Schema Definition**

A schema is defined for the incoming flight data to ensure proper parsing and validation. It includes fields such as flight ID, airline, departure and arrival details, passenger count, ticket price, and delay information.

**Reading Kafka Topics**

The application reads from three Kafka topics (east-coast-flights, west-coast-flights, and cross-country-flights). Each topic represents a specific data source, ensuring logical segregation of incoming data streams.

**Processing Data**

The streaming data is processed in the following steps:

**Parsing:** Kafka messages are deserialized and structured using the defined schema.
**Enrichment:** Additional fields such as route_name and event_time are added to enhance the data.
**Union:** Data from all topics is combined into a single DataFrame for unified processing.
**Analytics**

The application performs the following analytics on the streaming data:

Average ticket price and delay for each flight.

**Writing to Redis**

The aggregated results are written to a Redis cluster. Each record is stored as a hash, with keys and fields based on flight ID, route name, and time windows. This enables efficient querying and further processing of the analytics data.

**Key Features**

Real-time processing with watermarking to handle late-arriving data.

Batch processing with optimizations for high throughput.

Error handling to ensure resilience during Redis writes.

**Execution**

The streaming job is triggered every 30 seconds, ensuring timely updates to the Redis cluster.

### **kafka Producer**
To feed data into the Kafka topics, three producers have been configured. Each producer reads data from its respective source and writes to the designated Kafka topic:

**Cross Country Producer:** Configured in cross-country-producer.yaml, this producer sends data to the cross-country-flights Kafka topic.
**East Coast Producer:** Configured in east-coast-producer.yaml, this producer sends data to the east-coast-flights Kafka topic.
**West Coast Producer:** Configured in west-coast-producer.yaml, this producer sends data to the west-coast-flights Kafka topic.

### **Producer Features**
- **Data Randomization**: Simulates real-world flight scenarios with random parameters.
- **Efficiency**: Configured with batching, compression, and retries for performance.
- **Integration**: Writes JSON-encoded messages compatible with Kafka's schema requirements.

### **kubernetes RBAC setup**

This README provides details about setting up Kubernetes Role-Based Access Control (RBAC) for Apache Spark using the provided YAML configuration files.

**The RBAC setup consists of the following YAML files:**

**cluster-role-binding.yaml:** Defines cluster-level permissions binding a cluster role to a user, group, or service account.

**cluster-role.yaml:** Specifies cluster-wide access permissions for resources.

**pod-access-role.yaml:** Grants access permissions specific to pods.

**rolebinding-pod-access.yaml:** Binds the pod-access-role to a user or service account.

**service-account.yaml:** Defines a service account for the Spark application.

**spark-operator-role-binding.yaml:** Role binding for the Spark operator.

**spark-operator-role.yaml:** Role definition for the Spark operator.

**spark-rbac-setup.yaml:** Aggregates all RBAC components for streamlined setup.


### 📦 **Docker File**

The provided Dockerfile creates a containerized environment for running Apache Spark jobs written in Python.

**Base Image:** The base image used is apache/spark-py:3.4.0, which includes Apache Spark and Python.

**Working Directory:** The working directory is set to /opt/spark/work-dir/bob initially, then changed to /opt/spark/work-dir/airlines_data_analytics/src/jobs.

**Installing Python Dependencies:** Required Python libraries are installed from requirements.txt using pip3.

**Copying Scripts:** The feature_materializer.py script is copied to the container.

**Setting Permissions:** The spark_streaming.py script is given executable permissions.

### 🔄 **Data Load**

This Docker image supports loading data into a Redis database. Ensure that the required Python Redis library is specified in your requirements.txt file.