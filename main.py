#!/usr/bin/env python
"""
  -h, --help            show this help message and exit
  -n [int], --N [int]   Number of cases, [1,2,3,4...]
  -a {male,female,all}, --average-age {male,female,all}
                        Shows average female and male age,
                        ['male','female','all']
  -p {male,female}, --percent-gender {male,female}
                        Gives percents of female or male back in database
  -m {city,password}, --most-common {city,password}
                        Shows the most popular city and password. Optionally
                        we can add attribute -n, -N
  -dob [YYYY-MM-DD] [YYYY-MM-DD], --DOB [YYYY-MM-DD] [YYYY-MM-DD]
                        Shows the number of people who were born between
                        [start_data] and [end_data]
  -pr, --protect-password
                        Documentation
  -c, --create-database
                        Create database with '\data\persons.json'
"""
# Standard module
import argparse
import json
import os
from datetime import datetime

from tqdm import tqdm

# My module
import db

__author__ = "Dmytro Bohynskyi"
__version__ = "2.0.0"
__email__ = "bohynskyi@gmial.com"
__status__ = "Production"


# ---------------------------------------------------------------------
#                           -- Change data --
# ---------------------------------------------------------------------
def change_data(func):
    """
    The decorator creates fields with birth dates, delete "picture" and change number phone.
    """

    def wrapper(*args, **kwargs):
        data: dict = func(*args, **kwargs)
        for person in data['results']:
            # days until birth
            dob = person.get('dob', None)
            date = datetime.strptime(dob["date"], '%Y-%m-%dT%H:%M:%S.%fZ')
            dub = _days_until_birth(date)
            person["dob"]["dob"] = dub

            # correct number
            person['phone'] = _correct_phone_number(person.get('phone'))
            person['cell'] = _correct_phone_number(person.get('cell'))

            # delete 'picture'
            del person['picture']
        return data

    return wrapper


def _correct_phone_number(phone: str) -> str:
    if phone:
        phone = phone.replace('-', '')
        phone = phone.replace(':', '')
        phone = phone.replace(' ', '')
        phone = phone.replace(')', '')
        phone = phone.replace('(', '')
    return phone


def _days_until_birth(dob: datetime, next_bd_year=None) -> int:
    """
    The function return amount of remained days since birth date
    :param next_bd_year: year next birth day
    :param dob: Day of birth
    :return: int
    """
    today_date = datetime.now()  # current time
    bd_year = today_date.year if not next_bd_year else next_bd_year

    # dob - day of birth
    if dob.month != 2 or dob.day != 29:
        next_dob = dob.replace(year=bd_year)  # day of birth this year
    else:
        next_dob = _leap_day(dob, bd_year)  #

    days = (next_dob - today_date).days

    # if the day of birth was already
    if days < 0:
        days = _days_until_birth(dob, next_bd_year=(bd_year + 1))

    return days


def _leap_day(dob: datetime, next_bd_year: int) -> datetime:
    """
    This function checks if it exists in the following year on February 29.
    If there is an error, we assume that the date of birth is March 1.
    """
    try:
        next_dob = dob.replace(year=next_bd_year)
    except ValueError:
        next_dob = dob.replace(year=next_bd_year, month=4, day=1)

    return next_dob


# ---------------------------------------------------------------------
#                           -- Create db --
# ---------------------------------------------------------------------
def create_db(func):
    """
    This decorator creates database.
    """

    def wrapper(*args, **kwargs):
        query: dict = func(*args, **kwargs)  # open .json
        # Init data base if he isn't in this dir.
        db.init_db() if db.DB_NAME not in os.listdir() else None
        # Create database
        for data in tqdm(query['results']):
            db.create_db(db.Person, data)  # creates new entry in Person table

        return query

    return wrapper


# ---------------------------------------------------------------------
#                          -- Load .json --
# ---------------------------------------------------------------------
@create_db
@change_data
def load_json(path_json: str = "data/persons.json") -> dict:
    """
    This function open .json and return dictionary with data
    """
    path_json = path_json
    # Open json file then encoding in utf8
    with open(path_json, encoding="utf8") as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    # ---------------------------------------------------------------------
    #                          -- ARGPARSE --
    # ---------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='List the options:')

    # Optionals
    parser.add_argument('-n', "--N", help="Number of cases, [1,2,3,4...]",
                        nargs=1, metavar="[int]", type=int, default=1)
    parser.add_argument("-a", "--average-age", help="Shows average female and male age, ['male','female','all']",
                        nargs=1, choices=["male", 'female', "all"])
    parser.add_argument("-p", "--percent-gender", help="Gives percents of female or male back in database",
                        nargs=1, choices=["male", 'female'])
    parser.add_argument('-m', "--most-common",
                        help="Shows the most popular city and password. Optionally we can add attribute -n, -N ",
                        nargs=1, choices=["city", 'password'])
    parser.add_argument('-dob', "--DOB",
                        help="Shows the number of people who were born between [start_data] and [end_data]",
                        nargs=2, metavar="[YYYY-MM-DD]", type=db.valid_date)
    parser.add_argument('-pr', "--protect-password", help="Shows the most safe password",
                        action="store_true")
    parser.add_argument('-c', "--create-database", help="Creates database with '\data\persons.json'",
                        action="store_true")

    args = parser.parse_args()

    if args.average_age:  # Shows average female and male age
        db.select_age(args.average_age)
    elif args.percent_gender:  # Gives percents of female or male
        db.select_percent(args.percent_gender)
    elif args.most_common:  # Shows the most popular city and password
        db.select_popular(args.N, args.most_common[0])
    elif args.DOB:  # Shows the number of people who
        db.select_days_born(args.Data_of_born[0], args.args.Data_of_born[1])
    elif args.protect_password:  # Creates database with '\data\persons.json'
        db.select_protect_password(args.N)
    elif args.create_database:
        load_json()
    else:
        load_json()
