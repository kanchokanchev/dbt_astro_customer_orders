
# 1. Build Docker Image
docker image build -f Dockerfile . -t kkanchevgemseek/python_3_10_custom_dbt


# 2. Run Docker Compose Service(s)
docker compose -p dbt_svc -f docker-compose.yml --env-file .env up -d


# 3. Terminate Docker Compose Service(s)
docker compose -p dbt_svc down
