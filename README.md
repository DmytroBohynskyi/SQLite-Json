# SQL_JSON
## Jak postawić projekt 
Project jest napisany przy wykorzystaniu standartowych modułów Python 3.7 biblioteki peewee, requests
oraz qdm.

Dla uruchomienia projektu jedynie trzeba skorzystać z poniższego polecenia.
```commandline
pip install -r requirements.txt
```

## Dostępne komendy
```commandline
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
 -ce, --create-entry   Creates entry with https://randomuser.me/api/
```
### Zapis pliku .json do bazy danych
Dla przeprowadzenia tej operacji używamy jedynie flagi ``-c`` albo ``--create-database``.

Prykład: 
```commandline
python main.py -c
python main.py --create-database
```
###  Najbardziej popularne miasto
Dla wyświetlenia najbardziej popularnego masta musimy użyć flagi ``-m city`` 
albo ``--most-common city``. Atrubuk ``-n`` oreśla liczbe wyświetlanych miast.

Prykład:
```commandline
python main.py -m city

--------------------------------
|city                |Number    |
--------------------------------
|Gisborne            |         7|
```
```commandline
python main.py -m city -n 5

--------------------------------
|city                |Number    |
--------------------------------
|Gisborne            |         7|
|Van                 |         5|
|Queanbeyan          |         5|
|Napier              |         5|
|Lower Hutt          |         5|
```

###  Najbardziej popularne hasło
Analogicznie jak i poprzednim podpunkcie tylko ``city`` zamieniamy na ``password``

Przykład:
```commandline
python main.py -m password

--------------------------------
|password            |Number    |
--------------------------------
|surf                |         3|
```
```commandline
python main.py -m password -n 5

--------------------------------
|password            |Number    |
--------------------------------
|surf                |         3|
|achtung             |         3|
|weasel              |         2|
|wassup              |         2|
|walton              |         2|
```

## Najbezpieczniejsze hasło
Używany fjage ``-pr, --protect-password`` oraz przy użyciu ``-n`` dodatkowo możemy uzyskać liste popularnych haseł.

Przykład:
```commandline
python main.py -pr
------------------------------------
|Password            |Protect level|
------------------------------------
|films+pic+galeries  |9            |
```
```commandline
python main.py -pr -n 3
------------------------------------
|Password            |Protect level|
------------------------------------
|films+pic+galeries  |9            |
|summer99            |7            |
|scooter1            |7            |
```

## Śriedni wiek
Używamy flagę ``-a`` oraz opcjonalnie: 'male','female','all'.

Przykład:
```commandline
python main.py -a male
The average age of ['male'] is 48
```

## Procent kobiet i mężczyzn
Podobnie jak i poprzednio tylko flaga ``-p``.

Przykład:
```commandline
python main.py -p male
['male']: 50.2 %
```

