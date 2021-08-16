import boto3

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


