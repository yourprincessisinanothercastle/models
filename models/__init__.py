from mongoengine import *


connect(
    name='test',
    username='user',
    password='12345',
    host='mongodb://admin:qwerty@localhost/production'
)