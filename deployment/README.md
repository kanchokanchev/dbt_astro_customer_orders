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

# Deploy the local dev environment and prepare dbt profile
.PHONY: deploy-dev
deploy-dev: sync-profiles sync-pipeline-tasks dbt-deploy-dev

# Destroy the local Astro dev environment
.PHONY: destroy-dev
destroy-dev: dbt-destroy-dev

# Deploy to Astro Cloud (after syncing profile)
.PHONY: deploy-cloud
deploy-cloud: sync-profiles sync-pipeline-tasks dbt-deploy-cloud

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
```

---

## 🧪 Usage Examples

- **Start local development:**
  ```bash
  make deploy-dev
  ```

- **Stop local environment:**
  ```bash
  make destroy-dev
  ```

- **Deploy dbt project to Astro Cloud:**
  ```bash
  make deploy-cloud
  ```

- **Sync profiles.yml manually:**
  ```bash
  make sync-profiles
  ```

---

## ✅ Summary of Targets

| Target           | Description                                   |
|------------------|-----------------------------------------------|
| `deploy-dev`     | Sync profiles and start Astro locally         |
| `destroy-dev`    | Kill local Astro container                    |
| `deploy-cloud`   | Deploy the dbt project to Astronomer Cloud    |
| `sync-profiles`  | Copy `profiles.yml` to your dbt project       |

---

🌟 You’re now ready to deploy and manage your Astro + dbt stack with ease!
