## 🚀 Kubernetes RBAC Setup

This repository contains the RBAC (Role-Based Access Control) configuration for a distributed streaming application using Apache Spark, Kafka, and Redis across three separate Kubernetes namespaces. The RBAC setup ensures proper authorization and access control for Spark operators, cluster management, and pod lifecycle management.


## 👨‍💻 Tasks Overview

### 1. Service Account Setup
- Created a dedicated service account `spark-service-account` in the `spark-streaming-jobs` namespace
- This account serves as the identity for Spark applications running in the cluster

### 2. Cluster-Wide Permissions
- Implemented ClusterRole `spark-cluster-role` with permissions for:
  - Pod, service, configmap, and persistent volume claim management
  - Node monitoring and access capabilities
- Created ClusterRoleBinding to associate the service account with cluster-wide permissions
- Enables Spark to manage resources across the entire cluster

### 3. Namespace-Specific Access Control
- Configured Role `spark-pod-reader` for pod-specific operations within `spark-streaming-jobs` namespace
- Set up permissions for:
  - Pod lifecycle management (create, get, list, watch, delete)
  - Pod log access and monitoring
- Established corresponding RoleBinding to enforce these permissions

### 4. Spark Operator Configuration
- Implemented Role `spark-operator-role` with specific permissions for:
  - Managing SparkApplications and ScheduledSparkApplications
  - Handling core Kubernetes resources (pods, services, configmaps)
- Created RoleBinding `spark-operator-role-binding` to associate with `spark-operator` service account

### 5. Cross-Namespace Communication
- RBAC configuration enables secure communication between:
  - Kafka namespace (containing ZooKeeper, producer, and broker)
  - Spark application namespace
  - Redis namespace

## 📸 Snapshots
