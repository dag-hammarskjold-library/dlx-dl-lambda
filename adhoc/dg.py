import dlx_dl
import boto3
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
            '_id': 0, 
            'symbol': {
                '$arrayElemAt': [
                    '$identifiers.value', 0
                ]
            }
        }
    }
])

symbols = []
for res in result:
    symbols.append(res['symbol'])

rids = []
for symbol in set(symbols):
    print("Processing {}".format(symbol))
    result = client['undlFiles']['bibs'].aggregate([
        {
            '$match': {
                '191.subfields.value': symbol
            }
        }, {
            '$project': {
                '_id': 1
            }
        }
    ])
    rids.append(result['_id'])

'''
for rid in rids:
    try:
        dlx_dl.main(
            connect=connect_string,
            type='bib',
            modified_within=300,
            api_key=api_key,
            log=connect_string,
            nonce_key=nonce_key,
            callback_url=callback_url
        )
    except:
        raise
'''