FROM quay.io/astronomer/astro-runtime:12.9.0

# Install dbt
RUN pip install --no-cache-dir \
    dbt-core \
    dbt-snowflake \
    pandas \
    requests \
    dotenv \
    boto3 \
    snowflake-connector-python[pandas]
