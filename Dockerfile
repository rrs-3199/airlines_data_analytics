# Set the base image to use for the Docker image being built
FROM apache/spark-py:3.4.0

# Set the working directory inside container
WORKDIR /opt/spark/work-dir/bob

# Install required Python libraries
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy specified set of scripts and modules from the host to current working directory
COPY ./src/v2/jobs/feature_materializer.py /opt/spark/work-dir/airlines_data_analytics/src/jobs/

WORKDIR /opt/spark/work-dir/airlines_data_analytics/src/jobs

# Change the permission of streaming jobs to make them executable within the container
RUN chmod 777 spark_streaming.py