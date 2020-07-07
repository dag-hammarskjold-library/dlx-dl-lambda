import dlx_dl
import boto3
import re
#from tqdm import tqdm
from pymongo import MongoClient

ssm_client = boto3.client('ssm')
connect_string = ssm_client.get_parameter(Name='connect-string')['Parameter']['Value']
api_key = ssm_client.get_parameter(Name='undl-dhl-metadata-api-key')['Parameter']['Value']
nonce_key = ssm_client.get_parameter(Name='undl-callback-nonce')['Parameter']['Value']
callback_url = ssm_client.get_parameter(Name='undl-callback-url')['Parameter']['Value']

dlx_client = MongoClient(connect_string)
result = dlx_client['undlFiles']['files'].aggregate([
    {
        '$match': {
            'source': 'adhoc::digitization'
        }
    }, {
        '$project': {
            '_id': 1, 
            'symbol': {
                '$arrayElemAt': [
                    '$identifiers.value', 0
                ]
            }
        }
    }
])

dg_symbols = []
for res in result:
    dg_symbols.append({
        'symbol': res['symbol'],
        'bare': re.sub("/", "", res['symbol']).lower()
    })

result = dlx_client['undlFiles']['bibs'].aggregate([
    {
        '$project': {
            '_id': 1, 
            'symbol': {
                '$arrayElemAt': [
                    '$191.subfields.value', 0
                ]
            }
        }
    }
])
bib_symbols = []
for res in result:
    print(res)
    '''
    bib_symbols.append({
        'symbol': res['symbol'],
        'bare': re.sub("/", "", res['symbol']).lower()
    })
    '''