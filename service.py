import dlx_dl

def handler(event, context):
    coll = event['coll']
    print("Processing {}".format(coll))
    try:
        dlx_dl.run(
            type=coll,
            source='dlx-dl-lambda',
            modified_since_log=True,
            queue=300,
            use_api=True
        )
    except Exception as exc:
        print('; '.join(str(exc).split('\n')))
