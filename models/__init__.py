from mongoengine import *


db = connect(
    host='mongodb://localhost:27017/worldmap'
)