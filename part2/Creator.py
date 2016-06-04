'''
Exemplo recolhido na Internet e adaptado
'''
import boto3
import random

swf = boto3.client('swf',
                        aws_access_key_id='',
                        aws_secret_access_key='',
                        region_name='eu-west-1')

s3 = boto3.client('s3',
                  aws_access_key_id='',
                  aws_secret_access_key='')

DOMAIN = "project2es"
WORKFLOW = "MyTypeWF"
TASKNAME = "compute"
VERSION = "1"
TASKLIST = "MyTaskList"

number = input('Enter number: ')
name = input('Enter name of text file: ') + '.txt'  # Name of text file coerced with +.txt

file = open(name, 'w')  # Trying to create a new file or open one
file.write(number)
file.close()

s3.upload_file(name, 'ucesproject2', name)

response = swf.start_workflow_execution(
                                        domain=DOMAIN,
                                        workflowId='test-1019',
                                        workflowType={
                                                      "name": WORKFLOW,
                                                      "version": VERSION
                                                      },
                                        taskList={
                                                  'name': TASKLIST
                                                  },
                                        input=str(name)
                                        )
#print("Workflow requested: ", response)
s3.download_file('ucesproject2', response+'.txt', response)
s3.delete_objects(
    Bucket='ucesproject2',
    Delete={
        'Objects': [
            {
                'Key': response
            },
            {
                'Key': name
            },
        ],
        'Quiet': True
    }
)

print('Done')