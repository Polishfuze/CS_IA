import boto3
import hashlib

def getStudentsNormal():
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Students_Table')
    response = table.scan()
    return response['Items']


def getAllMovement():
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Movement_Table')
    response = table.scan()
    return response['Items']

def checkIfStudentExists(name):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table1 = dynamodb.Table('CSIA_Students_Table')
    table2 = dynamodb.Table('CSIA_Programming_Table')
    response1 = table1.get_item(Key={'StudentName': f'{name}'})
    response2 = table2.get_item(Key={'StudentName': f'{name}'})
    # print(response)
    return 'Item' in response1 or 'Item' in response2

def addStudentsToProg(name, teacher):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Programming_Table')
    UIDHasher = hashlib.sha256()
    UIDHasher.update(f"UID{name[::-1]}".encode())
    UID = UIDHasher.hexdigest()
    data = {
        'StudentName': f'{name}',
        'HeadTeacher': f'{teacher}',
        'UID': f'{UID}',
    }
    table.put_item(Item=data)
    return

def getAllTeachers():
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Login_Table')
    response = table.scan()
    print(response['Items'])
    teachers = []
    for acc in response['Items']:
        if 'teacher' in acc['roles']:
            teachers.append(acc['username']) 
    return list(set(teachers))



if __name__ == '__main__':
    print(getAllTeachers())
    pass