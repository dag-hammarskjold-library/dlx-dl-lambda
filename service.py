import dlx_dl
import boto3
from threading import Thread

ssm_client = boto3.client('ssm')
connect_string = ssm_client.get_parameter(Name='connect-string')['Parameter']['Value']
api_key = ssm_client.get_parameter(Name='undl-dhl-metadata-api-key')['Parameter']['Value']
nonce_key = ssm_client.get_parameter(Name='undl-callback-nonce')['Parameter']['Value']
callback_url = ssm_client.get_parameter(Name='undl-callback-url')['Parameter']['Value']

# dlx-dl --connect=$UNDLFILES --type=bib --modified_within=8640 --preview

'''
import dlx_dl

dlx_dl.main(connect='<connection_string>', type='bib', modified_from='2020-04-06Z00:00', api_key='<api_key>')

data = dlx_dl.LOG_DATA
'''

def handler(event, context):
    try:
        Thread(
            target=dlx_dl.main,
            kwargs = {
                'connect': connect_string,
                'type': 'bib',
                'modified_within': 300,
                'api_key': api_key,
                'log': connect_string,
                'nonce_key': nonce_key,
                'callback_url': callback_url,
            }
        ).start()
    
        Thread(
            target= dlx_dl.main,
            kwargs =  {
                'connect': connect_string,
                'type': 'auth',
                'modified_within': 300,
                'api_key': api_key,
                'log': connect_string,
                'nonce_key': nonce_key,
                'callback_url': callback_url,
            }
        ).start()
        
        return {
            'statusCode': 200,
            'body': 'Update complete.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
