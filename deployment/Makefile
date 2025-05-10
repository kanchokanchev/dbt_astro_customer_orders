# ========================================
# 🔧 Path Definitions
# ========================================

# Root of your local project workspace (one level above this Makefile)
WORKSPACE_ROOT_DIR := ../

# Airflow (Astro) and dbt directory paths
ASTRO_ROOT_DIR := $(WORKSPACE_ROOT_DIR)/airflow
DBT_ROOT_DIR := $(WORKSPACE_ROOT_DIR)/dbt

# Path to the dbt project and its profiles file
DBT_PROJECT_DIR := $(DBT_ROOT_DIR)/dbt_astro_demo
PROFILES_FILE := $(DBT_ROOT_DIR)/profiles.yml

# Mount path used during Astro Cloud deployment
MOUNT_PATH := /usr/local/airflow/dbt

# ========================================
# 🔨 Main Targets
# ========================================

# Deploy the local dev environment and prepare dbt profile
.PHONY: deploy-dev
deploy-dev: sync-profiles dbt-deploy-dev

# Destroy the local Astro dev environment
.PHONY: destroy-dev
destroy-dev: dbt-destroy-dev

# Deploy to Astro Cloud (after syncing profile)
.PHONY: deploy-cloud
deploy-cloud: sync-profiles dbt-deploy-cloud

# ========================================
# 🔁 Utilities
# ========================================

# Copy the shared profiles.yml into the dbt project directory
.PHONY: sync-profiles
sync-profiles:
	@echo "🔄 Syncing profiles.yml into dbt project directory..."
	cp $(PROFILES_FILE) $(DBT_PROJECT_DIR)/profiles.yml
	@echo "✅ profiles.yml copied to $(DBT_PROJECT_DIR)/profiles.yml"

# ========================================
# 🚀 Astro Local Development Commands
# ========================================

# Start the local Astro dev environment
dbt-deploy-dev:
	@echo "🚀 Starting Astro dev environment locally..."
	cd $(ASTRO_ROOT_DIR) && astro dev start
	@echo "✅ Local dev environment started!"

# Stop and remove the local Astro dev environment
dbt-destroy-dev:
	@echo "🚀 Killing Astro dev environment locally..."
	cd $(ASTRO_ROOT_DIR) && astro dev kill
	@echo "✅ Local dev environment removed!"

# ========================================
# ☁️ Astro Cloud Deployment
# ========================================

# Deploy the dbt project to Astro Cloud using the mount path
dbt-deploy-cloud:
	@echo "🚀 Deploying dbt project to Astro Cloud..."
	astro dbt deploy \
		--project-path $(DBT_PROJECT_DIR) \
		--mount-path $(MOUNT_PATH)
	@echo "✅ Cloud deployment complete!"
