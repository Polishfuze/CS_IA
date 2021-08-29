import boto3
from boto3.dynamodb.conditions import Key
from flask_bcrypt import Bcrypt

def verifyPassword(username, password):
    bcrypt = Bcrypt()
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Login_Table')
    response = table.get_item(Key={'username': username.lower()})
    print(response)
    try:
        passwordHash = response['Item']['password']
    except KeyError:
        return [False, []]
    roles = []
    isThePasswordCorrect = bcrypt.check_password_hash(passwordHash, password)
    if isThePasswordCorrect:
        roles = response['Item']['roles'].split(sep='&')
    return [isThePasswordCorrect, roles]


def registerUser(username, email, password):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    bcrypt = Bcrypt()
    table = dynamodb.Table('CSIA_Login_Table')
    data = {
        'username': username.lower(),
        'password': bcrypt.generate_password_hash(password).decode('utf-8'),
        'email': email.lower(),
        'roles': "",
    }
    table.put_item(Item=data)
    return


def checkIfUsernameExists(username):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Login_Table')
    response = table.get_item(Key={'username': username.lower()})
    # print(response)
    return 'Item' in response


def checkIfEmailExists(email):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Login_Table')
    scan_kwargs = {
        'FilterExpression': Key('email').eq(email.lower())
    }
    response = table.scan(**scan_kwargs)
    # print(response)
    if response['Count'] == 0:
        return False
    else:
        return True


def getUserData(username):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('CSIA_Login_Table')
    response = table.get_item(Key={'username': username.lower()})
    return response['Item']

if __name__ == '__main__':
    pass