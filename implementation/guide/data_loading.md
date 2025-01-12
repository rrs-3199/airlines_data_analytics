## 🚀 Data Loading

Redis serves as our high-performance data store, enabling real-time access to processed flight analytics with sub-millisecond latency. The in-memory nature of Redis ensures quick retrieval of recent flight metrics for immediate analysis and reporting.

## 👨‍💻 Tasks Overview

**Data Storage Operations**
- Created dedicated hash structures for each flight route:
  - `east_coast_metrics`: Stores East Coast flight analytics
  - `west_coast_metrics`: Maintains West Coast flight metrics
  - `cross_country_metrics`: Houses cross-country flight data
- Implemented data validation before storage
- Utilized Redis commands for data management:
  - `HSET`: Loading processed analytics results
  - `HGET`: Retrieving specific metric values
  - `HGETALL`: Fetching complete analytics for a route
  - `HSCAN`: Scanning through stored metrics efficiently

**Redis Kubernetes Setup**
1. **Configuration Setup**
   - Deployed Redis ConfigMap for custom configurations
   - Created Secrets for secure password management
   - Configured persistence settings for data durability

2. **Deployment Structure**
   - Implemented StatefulSet for stable pod identity
   - Set up headless service for pod discovery
   - Configured resource limits and requests
   - Established persistent volume claims for data storage

3. **Access Management**
   - Created external service for application access
   - Implemented proper RBAC permissions
   - Set up monitoring and health checks

## 📸 Snapshots