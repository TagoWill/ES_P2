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

def see_queue():
    flag = False
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

    print("Teste: " + msg.get("Messages")[0].get("MessageId") + "\nlol\n" + msg.get("Messages")[0].get("Body"))
    sqs.delete_message(
        QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/input',
        ReceiptHandle=msg.get("Messages")[0].get("ReceiptHandle")
    )
    sqs.send_message(
        QueueUrl='https://sqs.eu-west-1.amazonaws.com/561066985079/output',
        MessageBody=msg.get("Messages")[0].get("MessageId")+" - " +msg.get("Messages")[0].get("Body")
    )


def main():
    see_queue()


if __name__ == '__main__':
    main()
