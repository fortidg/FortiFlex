# How to use this script
This script will list all configurations in a given FortiFlex Program based on a provided Program Serial Number

You will need to provide three variables.  The script is written to look for them as environment variables.  If you want to use it as written, you will need to update your environment accordingly (example: export FORTICARE_USERNAME="FortiCare-username")
[This](https://docs.fortinet.com/document/forticloud/24.4.0/identity-access-management-iam/282341/adding-an-api-user) link will explain how to get the required credentials from FortiCare?

**FORTICARE_USERNAME**

**FORTICARE_PASSWORD**

The program Serial Number
**FORTIFLEX_SERIAL_NUMBER**

If you your FortiFlex Organization has multiple accounts, you can add "accountID" to the body of the request to get specific info for that account.  API docs found [here](https://fndn.fortinet.net/index.php?/fortiapi/954-fortiflex/3897/954/Configurations/)