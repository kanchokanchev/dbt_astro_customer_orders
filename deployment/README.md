# 🚀 Astro Cloud + dbt Deployment Automation

This guide documents a Makefile used to manage the local and cloud deployments of an **Astro (Airflow)** project integrated with a **dbt project**.

The workflow supports syncing profile configs, running local dev environments, and deploying to Astronomer Cloud.

---

## 📁 Project Structure

```
workspace-root/
├── airflow/                # Astro project directory
├── dbt/                    # dbt workspace
│   ├── dbt_astro_demo/     # dbt project
│   └── profiles.yml        # dbt profile config
└── Makefile                # (Stored inside deployment/ or similar)
```

---

## 🛠️ Makefile for dbt + Astro Integration

```makefile
# ========================================
# 🔧 Path Definitions
# ========================================

# Root of your local project workspace (one level above this Makefile)
WORKSPACE_ROOT_DIR := ../

# Airflow (Astro) and dbt directory paths
ASTRO_ROOT_DIR := $(WORKSPACE_ROOT_DIR)/airflow
ASTRO_INCLUDE_DIR := $(ASTRO_ROOT_DIR)/include

DBT_ROOT_DIR := $(WORKSPACE_ROOT_DIR)/dbt
PIPELINE_DIR := $(DBT_ROOT_DIR)/pipeline

# Path to the dbt project and its profiles file
DBT_PROJECT_DIR := $(DBT_ROOT_DIR)/dbt_astro_demo
PROFILES_FILE := $(DBT_ROOT_DIR)/profiles.yml
PIPELINE_TASKS_FILE := $(PIPELINE_DIR)/pipeline_tasks.py

# Mount path used during Astro Cloud deployment
MOUNT_PATH := /usr/local/airflow/dbt

# ========================================
# 🔨 Main Targets
# ========================================

# Deploy the local dbt dev environment
.PHONY: deploy-dbt-dev
deploy-dbt-dev: dbt-deploy-dev

# Destory the local dbt dev environment
.PHONY: destroy-dbt-dev
destroy-dbt-dev: dbt-destroy-dev

# Deploy the local Astro dev environment and prepare dbt profile
.PHONY: deploy-astro-dev
deploy-astro-dev: sync-profiles sync-pipeline-tasks astro-deploy-dev

# Destroy the local Astro dev environment
.PHONY: destroy-astro-dev
destroy-astro-dev: astro-destroy-dev

# Deploy to Astro Cloud (after syncing profile)
.PHONY: deploy-astro-cloud
deploy-astro-cloud: sync-profiles sync-pipeline-tasks astro-deploy-cloud

# ========================================
# 🔁 Utilities
# ========================================

# Copy the shared profiles.yml into the dbt project directory
.PHONY: sync-profiles
sync-profiles:
	@echo "🔄 Syncing profiles.yml into dbt project directory..."
	cp $(PROFILES_FILE) $(DBT_PROJECT_DIR)/profiles.yml
	@echo "✅ profiles.yml copied to $(DBT_PROJECT_DIR)/profiles.yml"

# Copy the pipeline_tasks.py into the airflow/include directory
.PHONY: sync-pipeline-tasks
sync-pipeline-tasks:
	@echo "🔄 Syncing profiles.yml into dbt project directory..."
	cp $(PIPELINE_TASKS_FILE) $(ASTRO_INCLUDE_DIR)/pipeline_tasks.py
	@echo "✅ pipeline_tasks.py copied to $(ASTRO_INCLUDE_DIR)/pipeline_tasks.py"


# ========================================
# 	dbt Local Development Commands
# ========================================

# Start the local dbt dev environment
dbt-deploy-dev:
	docker compose -p dbt_svc -f docker-compose.yml --env-file .env up -d

# Stop and remove the local dbt dev environment
dbt-destroy-dev:
	docker compose -p dbt_svc down


# ========================================
# 🚀 Astro Local Development Commands
# ========================================

# Start the local Astro dev environment
astro-deploy-dev:
	@echo "🚀 Starting Astro dev environment locally..."
	cd $(ASTRO_ROOT_DIR) && astro dev start
	@echo "✅ Local dev environment started!"

# Stop and remove the local Astro dev environment
astro-destroy-dev:
	@echo "🚀 Killing Astro dev environment locally..."
	cd $(ASTRO_ROOT_DIR) && astro dev kill
	@echo "✅ Local dev environment removed!"

# ========================================
# ☁️ Astro Cloud Deployment
# ========================================

# Deploy the dbt project to Astro Cloud using the mount path
astro-deploy-cloud:
	@echo "🚀 Deploying dbt project to Astro Cloud..."
	astro dbt deploy \
		--project-path $(DBT_PROJECT_DIR) \
		--mount-path $(MOUNT_PATH)
	@echo "✅ Cloud deployment complete!"
```

---

## 🧪 Usage Examples

- **Start dbt local dev environment:**
  ```bash
  make deploy-dbt-dev
  ```

- **Stop dbt local dev environment:**
  ```bash
  make destroy-dbt-dev
  ```

  - **Start Astro local dev environment:**
  ```bash
  make deploy-astro-dev
  ```

- **Stop Astro local dev environment:**
  ```bash
  make destroy-astro-dev
  ```

- **Deploy dbt project to Astro Cloud:**
  ```bash
  make deploy-astro-cloud
  ```

- **Sync profiles.yml manually:**
  ```bash
  make sync-profiles
  ```

- **Sync pipeline_tasks.py manually:**
  ```bash
  make sync-pipeline-tasks
  ```
---

## ✅ Summary of Targets

| Target                | Description                                          |
|-----------------------|------------------------------------------------------|
| `deploy-dbt-dev`      | Start dbt locally                                    |
| `destroy-dbt-dev`     | Kill local dbt container                             |
| `deploy-astro-dev`    | Sync profiles and start Astro locally                |
| `destroy-astro-dev`   | Kill local Astro containers                          |
| `deploy-astro-cloud`  | Deploy the dbt project to Astronomer Cloud           |
| `sync-profiles`       | Copy `profiles.yml` to your dbt project              |
| `sync-pipeline-tasks` | Copy `pipeline_tasks.py` into airflow/include folder |

---
