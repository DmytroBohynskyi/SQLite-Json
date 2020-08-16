# Standard module
import argparse
import string
from datetime import datetime

# My module
from peewee import fn

from models import *

DICT_TABLE_NAME = {
    'name': Name,
    'location': Location,
    'street': Street,
    'coordinates': Coordinates,
    'timezone': Timezone,
    'id': Id,
    'registered': Registered,
    'login': Login,
    'dob': DOB,
}


# ---------------------------------------------------------------------
#                           -- CREATE --
# ---------------------------------------------------------------------
def create_db(db_table, db_table_data: dict) -> int:
    """
    The function save data in the database table
    :param db_table: Table to which the data will be written do [Person, Name, Location, ...] (object of Model class)
    :param db_table_data: Data to be written to the table
    :return: Column Id in the table.
    """

    for entry_name in db_table_data:  # entry name in

        entry_in_table = db_table_data.get(entry_name, "None")
        # if entry_in_table if dictionary type then create new entry in the appropriate table
        if type(entry_in_table) == dict:
            sub_table = DICT_TABLE_NAME.get(entry_name)  # looking object for entry_name
            table_id = create_db(sub_table, entry_in_table)  # |Recurrence| Create new entry in sub_table
            db_table_data[entry_name] = table_id.id  # save sub_table id
        else:
            db_table_data[entry_name] = entry_in_table if entry_in_table else "None"
    # Save entry in db_table
    db_table_object = db_table.get_or_create(**db_table_data)[0]

    return db_table_object


# ---------------------------------------------------------------------
#                           -- SQLITE TABLE --
# ---------------------------------------------------------------------
@db.func()
def password_protect(password: str) -> int:
    protect_level = [0, 0, 0, 0, 0]
    if len(password) >= 8:
        protect_level[4] = 5
    for n in password:
        if n.islower():
            protect_level[0] = 1
        elif n.isupper():
            protect_level[1] = 2
        elif n.isalnum():
            protect_level[2] = 1
        elif n in string.punctuation:
            protect_level[3] = 3

    return sum(protect_level)


# ---------------------------------------------------------------------
#                           -- SELECT --
# ---------------------------------------------------------------------
def select_percent(gender: str) -> None:
    """
    This function gives percents of female or male back in database
    :param gender: "female' or "male
    :return: None
    """
    # Checking the number
    query = Person.select(Person.gender).where(Person.gender == "male").count()  # number of male
    count_person = Person.select().count()  # number of female

    percent = (query / count_person) * 100
    print(f"{gender}: {percent} %")


def select_age(gender: str) -> None:
    """
    This function shows percents of female or male back in database
    :param gender: "female' , "male" or "all"
    :return:
    """
    if gender != 'all':
        query = (Person
                 .select(fn.avg(DOB.age).alias('age'))
                 .join(DOB)
                 .where(Person.gender == gender)).first()
    else:
        query = Person.select(fn.avg(DOB.age).alias('age')).join(DOB)

    print(f"The average age of {gender} is {query.age}")


def select_popular(number_of_responses: int, select_type: str) -> None:
    """
    Shows the most popular city and password
    """
    # creating a variable for the searched table
    select_table = Location if select_type == "city" else Login
    column_table = Location.city if select_type == "city" else Login.password

    query = (select_table
             .select(column_table.alias("column_name"), fn.Count(column_table).alias("select_sum"))
             .group_by(column_table)
             .order_by(fn.Count(column_table).desc())
             .limit(number_of_responses))

    print(f"{'-':-^32} \n|{f'{select_type}':20}|{'Number':10}|\n{'-':-^32}")
    for n in query:
        print(f"|{n.column_name:20}|{n.select_sum:10}|")


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = f"Not a valid date: '{s}'."
        raise argparse.ArgumentTypeError(msg)


def select_days_born(start_date: str, end_date: str) -> None:
    """
    Shows the number of people who were born between [start_data] and [end_data]
    """
    query = Person.raw(
        f"SELECT n.first, p.email, d.date FROM Person as p  "
        f"LEFT JOIN Name as n ON n.id = p.name_id "
        f"LEFT JOIN DOB as d ON (d.id = p.dob_id) "
        f"WHERE d.date > '{start_date}' AND d.date < '{end_date}'"
    )

    print(f"|{'First Name':15}|{'Email':50}|{'data of birth'}|")
    for n in query:
        print(f"|{n.first:15}|{n.email:50}|{n.date[:10]:13}|")


def select_protect_password(number: int = 1) -> None:
    """
    Shows the most safe password
    """
    query = (Login
             .select(Login.password, fn.password_protect(Login.password).alias('protect'))
             .group_by(Login.password)
             .order_by(fn.password_protect(Login.password).desc())
             .limit(number))

    print(f"{'-':-^36} \n|{'Password':20}|{'Protect level':13}|\n{'-':-^36}")
    for n in query:
        print(f"|{n.password:20}|{n.protect:13}|")


if __name__ == '__main__':
    select_percent('male')
