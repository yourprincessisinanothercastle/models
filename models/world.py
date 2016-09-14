from mongoengine import StringField, Document, IntField, ReferenceField


class World(Document):
    name = StringField(required=True)
    seed = IntField()
    tilesize = IntField()
    octaves = IntField()

    tiles = ReferenceField()

    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)


