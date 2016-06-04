'''
Exemplo recolhido na Internet e adaptado
'''
#!/usr/bin/python

import boto3
import os
from botocore.client import Config

botoConfig = Config(connect_timeout=50, read_timeout=70)
swf = boto3.client('swf',
                        aws_access_key_id='',
                        aws_secret_access_key='',
                        region_name='eu-west-1', config=botoConfig)

s3 = boto3.client('s3',
                  aws_access_key_id='',
                  aws_secret_access_key='')

DOMAIN = "project2es"
WORKFLOW = "MyTypeWF"
TASKNAME = "compute"
VERSION = "1"
TASKLIST = "MyTaskList"

def compute(theinput):
    s3.download_file('ucesproject2', theinput, os.path.join(os.path.dirname(__file__) + '/temp/', theinput))

    slited = theinput.split(".")
    print('work')
    file = open(os.path.join(os.path.dirname(__file__) + '/temp/', theinput), 'r')
    file2 = open(os.path.join(os.path.dirname(__file__) + '/temp/', slited[0] + 'done.txt'), 'w')
    file2.write('Done: ' + file.read())

    file2.close()
    file.close()
    s3.upload_file(os.path.join(os.path.dirname(__file__) + '/temp/', slited[0] + 'done.txt'), 'ucesproject2',
                   slited[0] + 'done.txt')

    return slited[0] + 'done.txt'

while True:
        print("Listening for Decision Tasks")
        task = swf.poll_for_activity_task(
                                          domain=DOMAIN,
                                          taskList={'name': TASKLIST},
                                          identity='worker-1')
        if 'taskToken' not in task:
            print("Poll timed out, no new task.  Repoll")
        else:
            theinput = str(task['input'])
            print("New task", task['taskToken'], "arrived with input = ", theinput)
            response = compute(theinput)
            swf.respond_activity_task_completed(
                                                taskToken=task['taskToken'],
                                                result=str(response)
                                                )

            print("Task Done")


