## Data Ingestion

Apache Kafka serves as our primary data source to handle high-volume, real-time flight data streaming from multiple regions. This enables us to process live flight information efficiently while ensuring data reliability and fault tolerance.

## 👨‍💻 Tasks Overview

### **Kafka Setup**

**zookeeper**
- Manages Kafka cluster coordination
- Handles broker leader election
- Maintains configuration state
- Ensures cluster stability

**producers**
- Custom producers for flight data injection
- Implements retry mechanisms
- Handles data serialization
- Includes monitoring hooks

**kafka-deploy**
- Multi-broker deployment on Kubernetes
- Configurable retention policies
- Resource allocation management
- High availability setup

### **Kafka Producers & Topics**

**cross_country_flights:** 
By collecting data across regional boundaries, this topic enables insights into broader national patterns and trends.

**east_coast_flights:** 
Data streams from the East Coast operations are handled by this topic. 

**west_coast_flights:** 
This topic processes information feeds originating from the Western coastal region.

## 📸 Snapshots