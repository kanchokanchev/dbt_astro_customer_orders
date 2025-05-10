# ========================================
# 📁 Key Paths Configuration
# ========================================

TIMESTAMP := $(shell date +%Y%m%d%H%M%S)

# Directory to store all RSA key files
KEY_DIR := auth/keys

BACKUP_DIR := $(KEY_DIR)/backup_$(TIMESTAMP)

# File paths for key materials
PRIVATE_KEY := $(KEY_DIR)/snowflake_private_key.pem       # Original PEM (PKCS#1) private key
PUBLIC_KEY := $(KEY_DIR)/snowflake_public_key.pem         # Corresponding public key
PRIVATE_KEY_P8 := $(KEY_DIR)/snowflake_private_key.p8     # PKCS#8 DER-encoded private key (required by Snowflake)
PRIVATE_KEY_B64 := $(KEY_DIR)/snowflake_private_key.b64   # Base64-encoded private key for use in Airflow/Astro variables

# ========================================
# 🔨 Main Targets
# ========================================

# Generate and convert RSA keys (both PEM and PKCS#8 formats)
.PHONY: generate-keys
generate-keys: gen-keys conv-key

.PHONY: rotate-keys
rotate-keys: backup-keys clean-up-keys generate-keys get-private-key
	@echo "🔄 RSA Key rotation complete. Don't forget to run 'make update-snowflake-key' if using Terraform!"

# Encode the private key into base64 (for secrets storage)
.PHONY: get-private-key

# Clean up all key-related files
.PHONY: clean-up-keys


# ========================================
# 🔐 Key Generation
# ========================================

# Generate a 4096-bit RSA private key and its public key
gen-keys:
	@if [ -f "$(PRIVATE_KEY)" ]; then \
		echo "⚠️  Private key already exists at $(PRIVATE_KEY). Delete it first or run 'make clean-up'."; \
		exit 1; \
	fi
	@echo "🔐 Generating 4096-bit RSA Private Key..."
	mkdir -p $(KEY_DIR)
	openssl genrsa -out $(PRIVATE_KEY) 4096
	@echo "📤 Generating Public Key from Private Key..."
	openssl rsa -in $(PRIVATE_KEY) -pubout -out $(PUBLIC_KEY)
	@echo "✅ Keys generated at $(KEY_DIR)"


# ========================================
# 🔁 Convert Private Key to PKCS#8 (DER)
# ========================================

# Convert the PEM private key to PKCS#8 DER format (required by Snowflake)
conv-key:
	@echo "🔁 Converting to PKCS#8 DER format for Snowflake..."
	openssl pkcs8 -topk8 -inform PEM -outform DER -in $(PRIVATE_KEY) -out $(PRIVATE_KEY_P8) -nocrypt
	@echo "✅ Private key (PKCS#8 DER) ready at $(PRIVATE_KEY_P8)"


# ========================================
# 🔁 Rotate Keys for Snowflake
# ========================================

# Backup current keys with timestamp
.PHONY: backup-keys
backup-keys:
	@if [ -f "$(PRIVATE_KEY)" ]; then \
		echo "🗂️ Backing up existing keys to $(BACKUP_DIR)..."; \
		mkdir -p $(BACKUP_DIR); \
		cp $(KEY_DIR)/* $(BACKUP_DIR)/; \
	else \
		echo "ℹ️ No existing keys to backup."; \
	fi


# ========================================
# 📦 Encode for Variable Storage
# ========================================

# Base64-encode the .p8 file for safe use in JSON/YAML secrets
get-private-key:
	@if [ ! -f "$(PRIVATE_KEY_P8)" ]; then \
		echo "⚠️  Private key $(PRIVATE_KEY_P8) does not exist. Run 'make generate-keys' first to generate it."; \
		exit 1; \
	fi
	@echo "📦 Encoding private key (.p8) to base64..."
	base64 -w 0 $(PRIVATE_KEY_P8) > $(PRIVATE_KEY_B64)
	@echo "✅ Encoded key saved to: $(PRIVATE_KEY_B64)"
	@echo "👉 Use the contents of this file in your Astro/Airflow variable."


# ========================================
# 🧹 Clean Up All Keys
# ========================================

# Remove all key files to start fresh
clean-up-keys:
	@echo "🧹 Cleaning generated keys..."
	rm -f $(PRIVATE_KEY) $(PUBLIC_KEY) $(PRIVATE_KEY_P8) $(PRIVATE_KEY_B64)
	@echo "🗑️ Cleaned."
