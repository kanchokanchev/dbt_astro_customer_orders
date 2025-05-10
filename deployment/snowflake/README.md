# 🔐 Snowflake Key Pair Authentication Setup for Automated Pipelines (Airflow/Astro Cloud)

This guide walks you through setting up **RSA key pair authentication** for a Snowflake user account used in automated pipelines (e.g., Astronomer, Airflow). It includes full automation via Makefiles.

---

## 📁 Directory Structure

```
deployment/
└── snowflake/
    └── auth/
        └── keys/
            ├── snowflake_private_key.pem       # Raw RSA private key (PKCS#1)
            ├── snowflake_public_key.pem        # Public key
            ├── snowflake_private_key.p8        # DER-encoded key for Snowflake
            └── snowflake_private_key.b64       # Base64-encoded .p8 for Airflow/Astro
```

---

## ✅ STEP 1: Generate a Secure RSA Key Pair

```bash
openssl genrsa -out auth/keys/snowflake_private_key.pem 4096
openssl rsa -in auth/keys/snowflake_private_key.pem -pubout -out auth/keys/snowflake_public_key.pem
```

---

## 🔁 STEP 2: Convert Private Key to PKCS#8 DER Format

```bash
openssl pkcs8 -topk8 -inform PEM -outform DER \
-in auth/keys/snowflake_private_key.pem \
-out auth/keys/snowflake_private_key.p8 -nocrypt
```

---

## 🔐 STEP 3: Assign Public Key to Snowflake User

```sql
-- Copy contents of the public key (base64 only, no header/footer)
ALTER USER airflow_pipeline_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqhki...';

-- Optional: Disable password login for service accounts
ALTER USER airflow_pipeline_user UNSET PASSWORD;
```

---

## 📦 STEP 4: Base64 Encode the Private Key

```bash
base64 -w 0 auth/keys/snowflake_private_key.p8 > auth/keys/snowflake_private_key.b64
```

Use the content in your Airflow/Astro variable:

```json
{
  "username": "KKANCHEV",
  "privateKey": "<BASE64_ENCODED_KEY>",
  "account": "tceywpq-dl63751",
  "role": "SQL_DEV",
  "warehouse": "COMPUTE_XS",
  "database": "TEST_DB",
  "schema": "DBT_ASTRO_KKANCHEV"
}
```

---

## 🧹 STEP 5: Clean Up Keys

```bash
make clean-up-keys
```

---

## 🛠️ Makefile for Key Management

Save the following as `deployment/snowflake/Makefile`:

```makefile
# ========================================
# 📁 Key Paths Configuration
# ========================================

# Directory to store all RSA key files
KEY_DIR := auth/keys

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
```

---

## ✅ Summary of Makefile Targets

| Target              | Description                                              |
|---------------------|----------------------------------------------------------|
| `make generate-keys` | Generates both PEM and PKCS#8 (DER) private/public keys |
| `make get-private-key` | Base64 encodes `.p8` file for secret manager/variables |
| `make clean-up-keys` | Removes all generated keys                              |

---

## 🔒 Security Tips

- Use a dedicated **service account** in Snowflake
- **Unset password** to force key-based login only for automation
- Rotate keys every 90 days
- Use Snowflake's `LOGIN_HISTORY` to monitor access
- Store keys in a **secure secrets manager** (not in source control!)

---

🎉 You're now set up for secure, automation-friendly authentication to Snowflake!
