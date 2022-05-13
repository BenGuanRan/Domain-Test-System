import mongoengine

class ConnetTest(mongoengine.Document):
    name = mongoengine.StringField(max_length=32)
    age = mongoengine.IntField(default=0)


