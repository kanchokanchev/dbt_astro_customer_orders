# Base image with Python 3.10
FROM python:3.10-slim

# Set env vars
ENV DBT_HOME=/opt/project/dbt_astro/dbt
ENV PATH="/root/.local/bin:$PATH"

# Install system deps (for dbt + debugging)
RUN apt-get update && apt-get install -y \
    curl git build-essential libpq-dev bash \
    && rm -rf /var/lib/apt/lists/*

# Install dbt & required packages
RUN pip install --no-cache-dir \
    dbt-core \
    dbt-snowflake \
    pandas \
    requests \
    boto3 \
    snowflake-connector-python[pandas]

# For S3 uploads via CLI
RUN apt-get update && apt-get install -y awscli

CMD [ "bash" ]
