from pipeline_tasks import load_env_vars, download_csv, \
    create_snowflake_connection, load_to_snowflake, run_dbt


if __name__ == '__main__':
    # 1. Load configuration
    config = load_env_vars()

    # 2. Download data
    df = download_csv(config['CSV_DATA_URL'])

    # 3. Connect and load to Snowflake
    conn = create_snowflake_connection(config)
    load_to_snowflake(config, df, conn)

    # 4. Run dbt pipeline
    run_dbt(dbt_project_directory='dbt_astro/dbt/dbt_astro_demo')
