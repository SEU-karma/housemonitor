from peewee import *

database = MySQLDatabase('db_lanmonitor', **{'host': 'localhost', 'password': 'seuevege', 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Lan(BaseModel):
    lanid = CharField(null=True)
    time = DateTimeField(null=True)
    user = CharField(null=True)

    class Meta:
        db_table = 'lan'

