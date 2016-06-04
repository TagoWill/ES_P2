import boto3
import time

sqs = boto3.client('sqs',
                   aws_access_key_id='AKIAJWPN2OL5UVXVHASA',
                   aws_secret_access_key='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',
                   region_name='eu-west-1'
                   )

s3 = boto3.client('s3',
                  aws_access_key_id='AKIAJWPN2OL5UVXVHASA',
                  aws_secret_access_key='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')

simpledb = boto3.client('sdb',
                        aws_access_key_id='AKIAJWPN2OL5UVXVHASA',
                        aws_secret_access_key='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',
                        region_name='eu-west-1'
                        )


workernumber = 0

# print(sqs.list_queues())

def see_queue():
    flag = False
    print('Find sqs')
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='item1',
        Attributes=[
            {
                'Name': 'worker',
                'Value': 'Waiting for message in input',
                'Replace': False
            },
        ],
    )
    while not flag:
        msg = sqs.receive_message(
            QueueUrl=' https://sqs.eu-west-1.amazonaws.com/561066985079/input',
            AttributeNames=[
                'All',
            ],
            MessageAttributeNames=[
                'string',
            ],
            MaxNumberOfMessages=1
        )
        if msg.get("Messages") is not None:
            flag = True

    # print("Teste: " + msg.get("Messages")[0].get("MessageId") + "\nlol\n" + msg.get("Messages")[0].get("Body"))
    print('delete sqs')
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='item1',
        Attributes=[
            {
                'Name': 'worker',
                'Value': 'Delete sqs: '+msg.get("Messages")[0].get("Body"),
                'Replace': False
            },
        ],
    )
    sqs.delete_message(
        QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/input',
        ReceiptHandle=msg.get("Messages")[0].get("ReceiptHandle")
    )
    splited = msg.get("Messages")[0].get("Body").split(":")
    namefile = splited[1].split('.')

    # print(splited)
    print('Download file from s3')
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='item1',
        Attributes=[
            {
                'Name': 'worker',
                'Value': 'Download s3: ' + msg.get("Messages")[0].get("Body"),
                'Replace': False
            },
        ],
    )
    s3.download_file('ucesproject2', splited[1], 'temp/' + splited[1])

    print('work')
    file = open('temp/' + splited[1], 'r')
    file2 = open('temp/' + namefile[0] + 'done.txt', 'w')
    file2.write('Done: ' + file.read())

    file2.close()
    file.close()
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='item1',
        Attributes=[
            {
                'Name': 'worker',
                'Value': 'working: ' + msg.get("Messages")[0].get("Body"),
                'Replace': False
            },
        ],
    )
    print('sleep')
    time.sleep(60)
    print('send done file to s3')
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='item1',
        Attributes=[
            {
                'Name': 'worker',
                'Value': 'Work done: upload to S3: ' + msg.get("Messages")[0].get("Body"),
                'Replace': False
            },
        ],
    )
    s3.upload_file('temp/' + namefile[0] + 'done.txt', 'ucesproject2', namefile[0] + 'done.txt')
    print('writes sqs')
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='item1',
        Attributes=[
            {
                'Name': 'worker',
                'Value': 'Write sqs output: ' + msg.get("Messages")[0].get("Body"),
                'Replace': False
            },
        ],
    )
    sqs.send_message(
        QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/output',
        MessageBody=msg.get("Messages")[0].get("MessageId") + "." + 'namefile:' + namefile[0] + 'done.txt'
    )
    print('done')


def see_workernumber():
    tabela = simpledb.select(
        SelectExpression='select * from logging'
    ).get('Items')[0].get('Attributes')[0].get('Value')
    workernumber = int(tabela)
    workernumber += 1
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='workers',
        Attributes=[
            {
                'Name': 'number',
                'Value': str(workernumber),
                'Replace': True
            },
        ],
    )


def main():
    #see_workernumber()
    while 1:
        see_queue()


if __name__ == '__main__':
    main()
