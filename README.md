# dlx-dl-lambda
DLX-DL Lambda Function

`git clone https://github.com/dag-hammarskjold-library/dlx-dl-lambda`

`pip install -r requirements.txt`

`lambda deploy`

* service.py : Lambda function that polls for updates from a dlx compliant database and sends them to an Invenio Record API.
* adhoc/ : contains some scripts that perform specific ad hoc imports and demonstrate the capabilities of the connected libraries.