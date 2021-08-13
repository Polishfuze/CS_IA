import boto3
from flask_bcrypt import Bcrypt

def verifyPassword(username, password):
    bcrypt = Bcrypt()
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('LoginTable')
    response = table.get_item(Key={'username':username.lower()})
    # print(response)
    passwordHash = response['Item']['password']
    isThePasswordCorrect = bcrypt.check_password_hash(passwordHash, password)
    return isThePasswordCorrect

def registerUser(username, email, password):
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
    bcrypt = Bcrypt()
    table = dynamodb.Table('LoginTable')
    data = {
        'username':username.lower(),
        'password': bcrypt.generate_password_hash(password).decode('utf-8'),
        'email':email.lower(),
        }
    table.put_item(Item=data)

if __name__ == '__main__':
    pass
    # registerUser('as', '123')
    # print(getPasswordHash('M@gmail'))