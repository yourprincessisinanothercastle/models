from mongoengine import StringField, Document, IntField, ReferenceField, ListField

from models.users.character import Character
from passlib.hash import pbkdf2_sha256


def get_user(name):
    u = User.objects.filter(name=name).first()
    if not u:
        return False
    return u


def create_user(name, password):
    if not get_user(name):
        u = User(name, password).save()
        return u
    else:
        return False


class User(Document):
    name = StringField(unique=True)
    characters = ListField(ReferenceField(Character))

    password_hash = StringField()

    def __init__(self, name, password, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.name = name

        # password format: $pbkdf2-digest$rounds$salt$checksum
        self.password = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)


    @property
    def password_digest(self):
        return self.password.split('$')[1].split('pbkdf2-')[1]

    @property
    def password_rounds(self):
        return self.password.split('$')[2]

    @property
    def password_salt(self):
        return self.password.split('$')[3]


    def verify(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def add_char(self, name):
        if Character.objects.filter(name=name):
            return False
        c = Character(name).save()
        return c