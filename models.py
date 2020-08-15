"""
Documentation
"""
from peewee import SqliteDatabase, CharField, IntegerField, Model, DateField, ForeignKeyField, DateTimeField

DB_NAME = 'people.db'
db = SqliteDatabase(DB_NAME)


# ===============================================================
# Person -> Name
class Name(Model):
    title = CharField()
    first = CharField()
    last = CharField()

    class Meta:
        database = db
        table_name = "name"


# ===============================================================
# Location -> Street
class Street(Model):
    number = IntegerField()
    name = CharField()

    class Meta:
        database = db
        table_name = "street"


# Location -> Coordinates
class Coordinates(Model):
    latitude = IntegerField()
    longitude = IntegerField()

    class Meta:
        database = db
        table_name = "coordinates"


# Location -> Timezone
class Timezone(Model):
    offset = CharField()
    description = CharField()

    class Meta:
        database = db
        table_name = "timezone"


# Person -> Location
class Location(Model):
    street = ForeignKeyField(Street)
    coordinates = ForeignKeyField(Coordinates)
    timezone = ForeignKeyField(Timezone)
    city = CharField()
    state = CharField()
    country = CharField()
    postcode = CharField()

    class Meta:
        database = db
        table_name = "location"


# ===============================================================
# Person -> Id
class Id(Model):
    name = CharField()
    value = CharField()

    class Meta:
        database = db
        table_name = "id"


# ===============================================================
# Person -> Registered
class Registered(Model):
    date = DateField()
    age = IntegerField()

    class Meta:
        database = db
        table_name = "registered"


# ===============================================================
# Person -> Login
class Login(Model):
    uuid = CharField()
    username = CharField()
    password = CharField()
    salt = CharField()
    md5 = CharField()
    sha1 = CharField()
    sha256 = CharField()

    class Meta:
        database = db
        table_name = "login"


# ===============================================================
# Person -> DOB
class DOB(Model):
    date = DateTimeField()
    age = IntegerField()
    dob = IntegerField()

    class Meta:
        database = db
        table_name = "dob"


# ===============================================================
class Person(Model):
    # ---------------------------
    gender = CharField()
    email = CharField()
    nat = CharField()
    cell = IntegerField()
    phone = IntegerField()

    # ---------------------------
    name = ForeignKeyField(Name)
    location = ForeignKeyField(Location)
    id = ForeignKeyField(Id)
    registered = ForeignKeyField(Registered)
    login = ForeignKeyField(Login)
    dob = ForeignKeyField(DOB)

    class Meta:
        database = db


def init_db():
    db.connect()

    db.drop_tables([Person, Name, Id, Registered, Login, DOB, Street, Coordinates, Timezone, Location], safe=True)
    db.create_tables([Person, Name, Id, Registered, Login, DOB, Street, Coordinates, Timezone, Location], safe=True)


if __name__ == '__main__':
    init_db()
