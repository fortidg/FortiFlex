# How to use this script
This script will search for active FortiFlex entitlement with a blank description for the specified configuration.

You will need to provide three variables.  The script is written to look for them as environment variables.  If you want to use it as written, you will need to update your environment accordingly (example: export FORTICARE_USERNAME="FortiCare-username")
[This](https://docs.fortinet.com/document/forticloud/24.4.0/identity-access-management-iam/282341/adding-an-api-user) link will explain how to get the required credentials from FortiCare?

**FORTICARE_USERNAME**
**FORTICARE_PASSWORD**

The numeric Configuration ID.  You will need to make an API call to get this.
**FORTIFLEX_CONFIG_ID**