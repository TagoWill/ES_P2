import boto3

sqs = boto3.client('sqs',
                   aws_access_key_id='AKIAJWPN2OL5UVXVHASA',
                   aws_secret_access_key='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',
                   region_name='eu-west-1'
                   )

s3 = boto3.client('s3',
                  aws_access_key_id='AKIAJWPN2OL5UVXVHASA',
                  aws_secret_access_key='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')


# print(sqs.list_queues())

def write(name):
    try:
        file = open(name, 'w')  # Trying to create a new file or open one
        file.write("Teste")
        file.close()

    except:
        print('Something went wrong! Can\'t tell what?')


def send_aws(name):
    s3.upload_file(name, 'ucesproject2', name)
    msg = sqs.send_message(
        QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/input',
        MessageBody='namefile: ' + name
    )
    # s3.upload_file(os.path.join(os.path.dirname(__file__) + application.config['UPLOAD_FOLDER'],
    #                            session['car'] + file_extension), 'esimages3bucket', session['car'] + file_extension)

    print("TESTE: " + msg.get('MessageId'))
    return msg.get('MessageId')


def wait_response(id):
    flag = False
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
            print("Fim: " + msg.get("Messages")[0].get("MessageId") + "\nlol\n" + msg.get("Messages")[0].get("Body"))
            sqs.change_message_visibility(
                QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/output',
                ReceiptHandle=msg.get("Messages")[0].get("ReceiptHandle"),
                VisibilityTimeout=0
            )
## okey. matar o processo que é seu

def main():
    print('Creating new text file')

    name = input('Enter name of text file: ') + '.txt'  # Name of text file coerced with +.txt
    write(name)
    id = send_aws(name)
    wait_response(id)


if __name__ == '__main__':
    main()
