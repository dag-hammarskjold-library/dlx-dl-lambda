import dlx_dl
import boto3

ssm_client = boto3.client('ssm')
connect_string = ssm_client.get_parameter(Name='connect-string')['Parameter']['Value']
api_key = ssm_client.get_parameter(Name='undl-dhl-metadata-api-key')['Parameter']['Value']
nonce_key = ssm_client.get_parameeter(Name='undl-callback-nonce')

# dlx-dl --connect=$UNDLFILES --type=bib --modified_within=8640 --preview

'''
import dlx_dl

dlx_dl.main(connect='<connection_string>', type='bib', modified_from='2020-04-06Z00:00', api_key='<api_key>')

data = dlx_dl.LOG_DATA
'''

def handler(event, context):
    try:
        for coll in ['bib','auth']:
            dlx_dl.main(
                connect=connect_string,
                type=coll,
                modified_within=300,
                api_key=api_key,
                log=connect_string,
                nonce_key=nonce_key
            )
        return {
            'statusCode': 200,
            'body': 'Update complete.'
        }
    except:
        return {
            'statusCode': 500,
            'body': 'Something went wrong.'
        }
