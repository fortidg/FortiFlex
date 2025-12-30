# FortiFlex Entitlements Scripts

This folder contains Python scripts for managing FortiFlex entitlements through the Fortinet API.

## Authentication Requirements

All scripts require the following environment variables for FortiCare authentication:
- **FORTICARE_USERNAME** - Your FortiCare account username
- **FORTICARE_PASSWORD** - Your FortiCare account password

[API User Setup Guide](https://docs.fortinet.com/document/forticloud/24.4.0/identity-access-management-iam/282341/adding-an-api-user)

## Available Scripts and Functions

### 1. list-entitlement.py
**Purpose**: List all entitlements for a specific configuration

**Functions**:
- `fauth()` - Authenticate with FortiCare and get OAuth token
- `requests_post()` - Generic POST request handler with logging
- `get_entitlements(access_token, config_id)` - Retrieve list of entitlements for a configuration

**Required Environment Variables**:
- `FORTIFLEX_CONFIG_ID` - Numeric Configuration ID

**Usage**:
```bash
export FORTIFLEX_CONFIG_ID="12345"
python3 list-entitlement.py
```

### 2. stop-entitlement.py
**Purpose**: Stop active entitlements that have blank descriptions

**Functions**:
- `fauth()` - Authenticate with FortiCare and get OAuth token  
- `requests_post()` - Generic POST request handler with logging
- `get_active(access_token, config_id)` - Get active entitlements with blank descriptions
- `stop_entitlements(access_token)` - Stop all active unassigned entitlements

**Required Environment Variables**:
- `FORTIFLEX_CONFIG_ID` - Numeric Configuration ID

**Usage**:
```bash
export FORTIFLEX_CONFIG_ID="12345"
python3 stop-entitlement.py
```

### 3. transfer-entitlement.py  
**Purpose**: Transfer entitlements between configurations and accounts

**Functions**:
- `fauth()` - Authenticate with FortiCare and get OAuth token
- `requests_post()` - Generic POST request handler with logging  
- `transfer_entitlement(access_token, serial_numbers_list=None)` - Transfer entitlements with optional serial number filtering

**Required Environment Variables**:
- `FORTIFLEX_SOURCE_CONFIG_ID` - Source configuration ID
- `FORTIFLEX_SOURCE_ACCOUNT_ID` - Source account ID
- `FORTIFLEX_TARGET_CONFIG_ID` - Target configuration ID  
- `FORTIFLEX_TARGET_ACCOUNT_ID` - Target account ID

**Optional Environment Variables**:
- `FORTIFLEX_SERIAL_NUMBERS` - Comma-separated list of serial numbers to transfer (e.g., "FGT123456,FGT789012")

**Usage**:
```bash
# Transfer all available entitlements
export FORTIFLEX_SOURCE_CONFIG_ID="12345"
export FORTIFLEX_SOURCE_ACCOUNT_ID="67890"  
export FORTIFLEX_TARGET_CONFIG_ID="54321"
export FORTIFLEX_TARGET_ACCOUNT_ID="09876"
python3 transfer-entitlement.py

# Transfer specific serial numbers
export FORTIFLEX_SERIAL_NUMBERS="FGT123456,FGT789012,FGT345678"
python3 transfer-entitlement.py
```

**Programmatic Usage**:
```python
from transfer_entitlement import transfer_entitlement, fauth

# Transfer specific entitlements
serial_list = ["FGT123456", "FGT789012"]
result = transfer_entitlement(fauth(), serial_list)
```

## Common Function Reference

### Authentication Functions
- **`fauth()`** - Present in all scripts. Authenticates with FortiCare OAuth service and returns access token.

### Utility Functions  
- **`requests_post(resource_url, json_body, headers, verify=True)`** - Generic POST request wrapper with comprehensive logging and error handling.

## Error Handling

All scripts include:
- Exception handling for authentication failures
- Logging for debugging API requests and responses
- Graceful handling of empty results
- Input validation for environment variables

## Logging

To enable detailed logging for debugging:
```python
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```