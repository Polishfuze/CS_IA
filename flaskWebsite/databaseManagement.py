import boto3
from boto3.dynamodb.conditions import Key
from flask_bcrypt import Bcrypt


def verifyPassword(username, password):
    bcrypt = Bcrypt()
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('LoginTable')
    response = table.get_item(Key={'username': username.lower()})
    # print(response)
    passwordHash = response['Item']['password']
    isThePasswordCorrect = bcrypt.check_password_hash(passwordHash, password)
    return isThePasswordCorrect


def registerUser(username, email, password):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    bcrypt = Bcrypt()
    table = dynamodb.Table('LoginTable')
    data = {
        'username': username.lower(),
        'password': bcrypt.generate_password_hash(password).decode('utf-8'),
        'email': email.lower(),
    }
    table.put_item(Item=data)


def checkIfUsernameExists(username):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('LoginTable')
    response = table.get_item(Key={'username': username.lower()})
    # print(response)
    if 'Item' in response:
        return True
    else:
        return False


def checkIfEmailExists(email):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('LoginTable')
    scan_kwargs = {
        'FilterExpression': Key('email').eq(email.lower())
    }
    response = table.scan(**scan_kwargs)
    # print(response)
    if response['Count'] == 0:
        return False
    else:
        return True


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


def createResetToken(username):
    pass


if __name__ == '__main__':
    pass
    print(getAllMovement())
    getStudentsNormal()
    print(checkIfEmailExists("michalek.raj@gmail.com"))
    print(checkIfEmailExists("michaadsdaslek.raj@gmail.com"))
    # registerUser('as', '123')
    # print(getPasswordHash('M@gmail'))
