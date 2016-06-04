import boto3

simpledb = boto3.client('sdb',
                        aws_access_key_id='AKIAJWPN2OL5UVXVHASA',
                        aws_secret_access_key='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',
                        region_name='eu-west-1')

cenas = simpledb.select(
    SelectExpression='select * from logging'
).get('Items')[1].get('Attributes')

#print(cenas)

for i in range(0, len(cenas)):
    print(cenas[i])
