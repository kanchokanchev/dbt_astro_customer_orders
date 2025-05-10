
# 1. Build Docker Image
docker image build -f Dockerfile . -t kkanchevgemseek/python_3_10_custom_dbt


# 2. Run Docker Compose Service(s)
export DOCKER_USER=$(echo ${USER} | sed 's/[\\.]/_/g' | tr '[:upper:]' '[:lower:]') && \
docker compose -p ${DOCKER_USER}_dbt_svc -f docker-compose.yml --env-file .env up -d


# 3. Terminate Docker Compose Service(s)
export DOCKER_USER=$(echo ${USER} | sed 's/[\\.]/_/g' | tr '[:upper:]' '[:lower:]') && \
docker compose -p ${DOCKER_USER}_dbt_svc down
