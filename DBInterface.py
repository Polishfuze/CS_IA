import urllib.request
import boto3
import time
import hashlib
from boto3.dynamodb.conditions import Key


def checkConnect():
    """This function checks the connection and the state of the AWS by pinging it and returning True when the ping is successful."""
    try:
        urllib.request.urlopen('https://aws.amazon.com/')
        return True
    except:
        return False


# The DB's are imagined to be constructed as such:
# Table1: |Movement Index|UID|Name|Movement|Timestamp
# Table2: |Name|UID|CurrentState
# Table3: |Username|Email|PasswordHash
# Table4: |Name|

def createTables(createTable1=True, createTable2=True, createTable3=True, createTable4=True):
    """Creates the required tables in dynamoDB, needs to be only ran once on initial deployment or in the event of a deletion of a table. 
    Table1 is the student movement table, it records every single proper (UID in the database) scan of the card, and allows to track when students are in and out of classes.
    Table2 is the student table it stores a lot of information, firstly the UID of each student and their name, it also stores their current state (in school or not).
    Table3 is the login table, it stores the username, email, and hashed passwords of the staff that have access to the website.
    Table4 is the studentProgramming table, it is very similar to the student table, besides lacking a UID, and the current state in it's data.
    By default this creates all tables.
    """
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    if createTable1:
        table = dynamodb.create_table(
            TableName='CSIA_Movement_Table',
            KeySchema=[
                {
                    'AttributeName': 'MovementID',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'StudentUID',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'MovementID',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'StudentUID',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 1
            }
        )
        table.meta.client.get_waiter('table_exists').wait(
            TableName='CSIA_Movement_Table')
        print('Table 1 was successfully created!')
    if createTable2:
        table = dynamodb.create_table(
            TableName='CSIA_Students_Table',
            KeySchema=[
                {
                    'AttributeName': 'StudentName',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
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
        table.meta.client.get_waiter('table_exists').wait(
            TableName='CSIA_Students_Table')
        print('Table 2 was successfully created!')
    if createTable3:
        table = dynamodb.create_table(
            TableName='CSIA_Login_Table',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        table.meta.client.get_waiter('table_exists').wait(
            TableName='CSIA_Login_Table')
        print('Table 3 was successfully created!')
    if createTable4:
        table = dynamodb.create_table(
            TableName='CSIA_Programming_Table',
            KeySchema=[
                {
                    'AttributeName': 'StudentName',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'StudentName',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        table.meta.client.get_waiter('table_exists').wait(
            TableName='CSIA_Programming_Table')
        print('Table 4 was successfully created!')


def GetAllStudents():
    """This function runs a scan on the Students Table to establish all the possible UID's and names and then returns them as a dict with key of UID and value of Name"""
    studentDict = {}
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Students_Table')
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    for dict in data:
        studentDict[dict['UID']] = dict['StudentName']

    return(studentDict)


def StudentChangedState(UID):
    """This function is used to update table2 and append table1"""
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    tableToUpdate = dynamodb.Table('CSIA_Students_Table')
    tableToAppend = dynamodb.Table('CSIA_Movement_Table')
    timeNow = time.time()

    # response = tableToAppend.scan(
    #     {'FilterExpression': Key('StudentUID').eq(UID)})
    scan_kwargs = {
        'FilterExpression': Key('StudentUID').eq(UID)
    }
    response = tableToAppend.scan(**scan_kwargs)
    name = response['Items'][0]['StudentName']
    prevMovement = response['Items'][0]['isInSchool']
    prevInd = response['Count']
    data = {
        'MovementID': int(prevInd),
        'StudentUID': UID,
        'StudentName': name,
        'isInSchool': not prevMovement,
        'Timestamp': int(timeNow)
    }
    tableToAppend.put_item(Item=data)

    response = tableToUpdate.get_item(Key={'StudentName': name})
    currState = ''
    prevState = response['Item']['State']

    if prevState == 'OutOfSchool':
        currState = 'InSchool'
    else:
        currState = 'OutOfSchool'
    data = {
        'StudentName': name,
        'Headteacher': response['Item']['Headteacher'],
        'State': currState,
        'UID': UID
    }
    print(data)
    tableToUpdate.put_item(Item=data)


def getStudentToProgram():
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Programming_Table')
    students = table.scan()['Items']
    return students[0]


def pullAllStudents():
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Students_Table')
    return table.scan()['Items']

def onSuccesfulProgram(name, teacher, uid):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Programming_Table')
    table.delete_item(Key={'StudentName': name})
    table = dynamodb.Table('CSIA_Movement_Table')
    data = {
        'StudentUID': uid,
        'MovementID': 0,
        'StudentName': f'{name}',
        'Timestamp': 0,
        'isInSchool': False,
        
    }
    table.put_item(Item=data)
    table = dynamodb.Table('CSIA_Students_Table')
    data = {
        'StudentName': f'{name}',
        'State': f'{0}',
        'Headteacher': f'{teacher}',
        'StudentUID': uid,
    }
    table.put_item(Item=data)
    pass


def isStudentPresent(studentID):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Movement_Table')
    response = table.scan(FilterExpression=Key('StudentUID').eq(str(studentID)))
    return response


def pushStudent(studentId, index=None, date=None, timeR=None, debug=False):
    isInSchool = True
    name = None
    if index is None:
        presentness = isStudentPresent(studentId)['Items']
        print(presentness)
        if debug:
            print(presentness)
        if presentness == []:
            index = -1
        else:
            from operator import itemgetter
            newlist = sorted(presentness, key=itemgetter(
                'MovementID'), reverse=True)
            index = newlist[0]['MovementID']
            isInSchool = newlist[0]['isInSchool']
            name = newlist[0]['StudentName']
    if date is None:
        date = int(time.time())
    print(
            f'Student ID: {studentId}, Index = {index+1}, they are in school? {isInSchool}')
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Movement_Table')
    studentJson = {'StudentUID': str(studentId),
                   'MovementID': index+1,
                   'StudentName': f'{name}',
                   'Timestamp': date,
                   'isInSchool': not isInSchool}
    table.put_item(Item=studentJson)
    return True
#


#
# def createStudent(name, studentId=None, debug=False):
#     dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
#     if studentId is None:
#         studentId = hash(name)
#     studentJson = {'StudentID' : str(studentId),
#                    'StudentName' : name}
#     table = dynamodb.Table('CSIAStudentsTable')
#     table.put_item(Item = studentJson)
#     if debug:
#         print(f'Student id is: {studentId}')
#     return studentId
if __name__ == '__main__':
    # dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    # createTables()
    # print(checkConnect())
    # print(GetAllStudents())
    # StudentChangedState('0001', 'Mike')
    # print(createStudent('Michal Rajzer'))
    # pushStudent('-42527281', debug=True)
    getStudentToProgram()
    pass
