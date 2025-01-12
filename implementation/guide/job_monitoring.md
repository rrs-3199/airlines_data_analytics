## 🚀 Job Monitoring

Monitoring the stability of PySpark Structured Streaming jobs is crucial to ensure data is processed efficiently and within the desired time frame. This can be achieved by using the Spark UI, which provides detailed insights into the execution of streaming jobs.

## 👨‍💻 Tasks Overview

Key metrics and visualizations available in the Spark UI include:

- **Executor Status**: Displays the health and resource utilization of executors.

- **Physical and Logical Plan Graphs**: Visual representations of the streaming job’s execution plan.

- **Incoming Data**: The rate at which data is received.

- **Processed Data**: The rate at which data is processed.

- **Batch Duration**: Time taken to process each micro-batch.

- **Operation Duration**: Time taken for individual operations within a batch.

- **Watermark Delays**: Lag in event-time watermarking for streaming data.


In this setup, the streaming job is configured to process data in 30-second batches. When all graphs show consistent and stable patterns, it indicates that the streaming job is functioning optimally. However, if the batch duration or operation duration graphs show exponential increases, this signals that the job is unstable and is unable to process incoming data on time.


## 📸 Snapshots