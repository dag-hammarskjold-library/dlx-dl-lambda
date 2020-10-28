import dlx_dl
import boto3
import traceback

ssm_client = boto3.client('ssm')
connect_string = ssm_client.get_parameter(Name='connect-string')['Parameter']['Value']
api_key = ssm_client.get_parameter(Name='undl-dhl-metadata-api-key')['Parameter']['Value']
nonce_key = ssm_client.get_parameter(Name='undl-callback-nonce')['Parameter']['Value']
callback_url = ssm_client.get_parameter(Name='undl-callback-url')['Parameter']['Value']

def handler(event, context):
    coll = event['coll']
    print("Processing {}".format(coll))
    try:
        dlx_dl.run(
            connect=connect_string,
            type=coll,
            #modified_within=300,
            api_key=api_key,
            #log=connect_string,
            nonce_key=nonce_key,
            callback_url=callback_url,
            source='dlx-dl-lambda',
            modified_since_log=True
        )
    except Exception as exc:
        traceback.print_exc()
        pass
