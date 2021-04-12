import urllib.request
import boto3
import time
import hashlib
from boto3.dynamodb.conditions import Key

def checkConnect():
    try:
        urllib.request.urlopen('https://aws.amazon.com/')
        return True
    except:
        return False

def createTables(create1 = True, create2 = True, create3 = True):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    if create1:
        table1 = dynamodb.create_table(
            TableName='CSIAStudentsTable',
            KeySchema=[
                {
                     'AttributeName': 'StudentID',
                     'KeyType': 'HASH'  
                },
                {
                    'AttributeName': 'StudentName',
                    'KeyType': 'RANGE'
                }
                ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'StudentID',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'StudentName',
                    'AttributeType': 'S'
                },
                ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 1
                }
            )
        table1.meta.client.get_waiter('table_exists').wait(TableName='CSIAStudentsTable')
        print(table1.item_count)
    if create2:
        table2 = dynamodb.create_table(
            TableName='CSIAMovementTable',
            KeySchema=[
                {
                    'AttributeName': 'indexNum',
                    'KeyType': 'HASH'
                },
                {
                     'AttributeName': 'StudentID',
                     'KeyType': 'RANGE'
                }
                ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'indexNum',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'StudentID',
                    'AttributeType': 'S'
                }
                ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
                }
            )
        table2.meta.client.get_waiter('table_exists').wait(TableName='CSIAMovementTable')
        print(table2.item_count)
    if create3:
        table3 = dynamodb.create_table(
            TableName='CSIAAddStudent',
            KeySchema=[
                {
                    'AttributeName': 'Name',
                    'KeyType': 'HASH'
                },
                {
                     'AttributeName': 'StudentID',
                     'KeyType': 'RANGE'
                }
                ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'StudentID',
                    'AttributeType': 'S'
                }
                ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
                }
            )
        table3.meta.client.get_waiter('table_exists').wait(TableName='CSIAAddStudent')
        print(table3.item_count)

def pullAllStudents():
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIAStudentsTable')
    return table.scan()


def pullStudentByID(studentID):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIAMovementTable')
    response = table.query(
    KeyConditionExpression=Key('StudentID').eq(studentID)
    )
    if response is not None:
        return response['item']
    else:
        return False

def isStudentPresent(studentID):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIAMovementTable')
    response = table.scan(FilterExpression=Key('StudentID').eq(str(studentID)))
    return response

def pushStudent(studentId, index=None, date=None, timeR=None, debug=False):
    isInSchool = True
    if index is None:
        presentness = isStudentPresent(studentId)['Items']
        if debug:
            print(presentness)
        if presentness == []:
            index = -1
        else:
            from operator import itemgetter
            newlist = sorted(presentness, key=itemgetter('indexNum'), reverse=True)
            index = newlist[0]['indexNum']
            isInSchool = newlist[0]['isInSchool']
    if date is None:
        date = time.localtime(time.time())[0:3]
        timeR = time.localtime(time.time())[3:6]
    if debug:
        print(f'Student ID: {studentId}, Index = {index+1}, they are in school? {isInSchool}')
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIAMovementTable')
    studentJson = {'indexNum' : index+1,
                   'StudentID' : str(studentId),
                   'Date' : date,
                   'Time' : timeR,
                   'isInSchool' : not isInSchool}
    table.put_item(Item = studentJson)
    return True

def getStudentToProgram():
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIAAddStudent')
    students = table.scan['Items']
    table.delete_item(Key=students[0])
    return students[0]

def createStudent(name, studentId=None, debug=False):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    if studentId is None:
        studentId = hash(name)
    studentJson = {'StudentID' : str(studentId),
                   'StudentName' : name}
    table = dynamodb.Table('CSIAStudentsTable')
    table.put_item(Item = studentJson)
    if debug:
        print(f'Student id is: {studentId}')
    return studentId

if __name__ == '__main__':
    print(checkConnect())
    # print(createStudent('Michal Rajzer'))
    # pushStudent('-42527281', debug=True)
    createTables(create1=False, create2=False, create3=False)
