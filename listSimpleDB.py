import boto3

simpledb = boto3.client('sdb',
                        aws_access_key_id='',
                        aws_secret_access_key='',
                        region_name='eu-west-1')

cenas = simpledb.select(
    SelectExpression='select * from logging'
).get('Items')[1].get('Attributes')

#print(cenas)

for i in range(0, len(cenas)):
    print(cenas[i])
