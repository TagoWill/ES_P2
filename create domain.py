import boto3

simpledb = boto3.client('sdb',
                        aws_access_key_id='AKIAJWPN2OL5UVXVHASA',
                        aws_secret_access_key='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',
                        region_name='eu-west-1')

simpledb.delete_domain(
    DomainName='logging'
)

simpledb.create_domain(
    DomainName='logging'
)

simpledb.put_attributes(DomainName='logging',
        ItemName='workers',
        Attributes=[
            {
                'Name': 'number',
                'Value': '0',
                'Replace': False
            },
        ],)

print(simpledb.list_domains().get('DomainNames'))
