import boto3

sqs = boto3.client('sqs',
                   aws_access_key_id='',
                   aws_secret_access_key='',
                   region_name='eu-west-1'
                   )

s3 = boto3.client('s3',
                  aws_access_key_id='',
                  aws_secret_access_key='')

simpledb = boto3.client('sdb',
                        aws_access_key_id='',
                        aws_secret_access_key='',
                        region_name='eu-west-1'
                        )


# print(sqs.list_queues())

def write(name, number):
    try:
        file = open(name, 'w')  # Trying to create a new file or open one
        file.write(number)
        file.close()

    except:
        print('Something went wrong! Can\'t tell what?')


def send_aws(name):
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='item1',
        Attributes=[
            {
                'Name': 'client',
                'Value': 'Add file to s3: '+name,
                'Replace': False
            },
        ],

    )
    s3.upload_file(name, 'ucesproject2', name)
    simpledb.put_attributes(
        DomainName='logging',
        ItemName='item1',
        Attributes=[
            {
                'Name': 'client',
                'Value': 'Writes on SQS input and wait on SQS output',
                'Replace': False
            },
        ],
    )
    msg = sqs.send_message(
        QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/input',
        MessageBody='namefile:' + name
    )
    # s3.upload_file(os.path.join(os.path.dirname(__file__) + application.config['UPLOAD_FOLDER'],
    #                            session['car'] + file_extension), 'esimages3bucket', session['car'] + file_extension)

    # print("TESTE: " + msg.get('MessageId'))
    return msg.get('MessageId')


def wait_response(oldnmae, id):
    flag = False
    print('wait')
    while not flag:
        msg = sqs.receive_message(
            QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/output',
            AttributeNames=[
                'All'
            ],
            MessageAttributeNames=[
                'string',
            ],
            MaxNumberOfMessages=1
        )
        if msg.get("Messages") is not None:

            splited = msg.get("Messages")[0].get("Body").split('.')
            namefile = splited[1].split(':')
            if splited[0] != id:
                sqs.change_message_visibility(
                    QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/output',
                    ReceiptHandle=msg.get("Messages")[0].get("ReceiptHandle"),
                    VisibilityTimeout=0
                )
            else:
                flag = True
                simpledb.put_attributes(
                    DomainName='logging',
                    ItemName='item1',
                    Attributes=[
                        {
                            'Name': 'client',
                            'Value': 'Delete SQS output',
                            'Replace': False
                        },
                    ],

                )
                sqs.delete_message(
                    QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/output',
                    ReceiptHandle=msg.get("Messages")[0].get("ReceiptHandle")
                )
                simpledb.put_attributes(
                    DomainName='logging',
                    ItemName='item1',
                    Attributes=[
                        {
                            'Name': 'client',
                            'Value': 'Download file form s3: '+namefile[1]+'.txt',
                            'Replace': False
                        },
                    ],

                )
                s3.download_file('ucesproject2', namefile[1]+'.txt', namefile[1]+'.txt')
                simpledb.put_attributes(
                    DomainName='logging',
                    ItemName='item1',
                    Attributes=[
                        {
                            'Name': 'client',
                            'Value': 'Delete files form s3',
                            'Replace': False
                        },
                    ],
                )
                s3.delete_objects(
                    Bucket='ucesproject2',
                    Delete={
                        'Objects': [
                            {
                                'Key': namefile[1]+'.txt'
                            },
                            {
                                'Key': oldnmae
                            },
                        ],
                        'Quiet': True
                    }
                )
                simpledb.put_attributes(
                    DomainName='logging',
                    ItemName='item1',
                    Attributes=[
                        {
                            'Name': 'client',
                            'Value': 'Done',
                            'Replace': False
                        },
                    ],

                )
                print('Done. File downloaded')


def main():
    print('Creating new text file')
    number = input('Enter number: ')
    name = input('Enter name of text file: ') + '.txt'  # Name of text file coerced with +.txt
    write(name, number)
    id = send_aws(name)
    wait_response(name, id)


if __name__ == '__main__':
    main()
