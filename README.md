# Coolest Districts API
- [Data Source](https://open-meteo.com/en/docs)
- API for the coolest 10 districts based on the average temperature at 2pm for the next 7 days.
- API where given location, destination, and the date of travel. A decision is given whether to travel or not based on the temperature of 2pm of both places.

## Dependencies
There is a few dependencies which are required to make the application work correctly:

| Name | Version |
| ------ | ------ |
| python | 3.11 |
| MySQL DB | 8.0.31 |
| Redis |  7.2.2 |

##### Important Points: 
+ As I have noticed the APIs are read heavy, writing does not affect the user experience as writing is mostly done from other API consumption. Due to this I chose a MySQL database for this
+ I have developed the projects on a windows machine and ran redis on WSL. I am writing the process from that perspective.

## Python Packages
The below listed python packages are also required.
| application | Version |
| ------ | ------ |
| pipenv | * |
| django | 4.2.6 |
| djangorestframework | 3.14.0 |
| mysqlclient | 2.2.0 |
| python-dotenv | 1.0.0 |
| requests | 2.31.0 |
| drf-spectacular | 0.26.5 |
| locust | 2.17.0 |
| celery | 5.3.4 |
| redis | 5.0.1 |
| django-celery-beat| 2.5.0 |
| django-celery-results | 2.5.1 |

## Installation
###### requires [python](https://www.python.org/) 3.11 & pipenv to run

First install the pipenv package with the below command
```sh
$ pip install pipenv
```
Install the dependency packages using the below command from pipfile.
```sh
$ pipenv install
```

## Running the Project

First you need to configure the dotenv file. I have provided the .env_example file. Rename it to .env and put the required parameters. Once the dotenv file has been configured please execute the below command to migrate the Database.
```sh
$ pipenv run python manage.py migrate
```

after running migration is if you face `django.db.utils.OperationalError: (1071, 'Specified key was too long; max key length is 1000 bytes')` please execute the below sql on your database.
```sh
$ ALTER DATABASE `databasename` CHARACTER SET utf8;
```

Alternatively, if you create your database with the below sql command. You wont face the error.
```sh
$ CREATE DATABASE `databasename` CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci; 
```

Create a super user using the below command.
```sh
$ pipenv run python manage.py createsuperuser
```

After that to load the initial data execute the below commands.
- first command will parse the `districts.json` file and push the districts data into the database.
- second command will use the districts longitude and latitude data, fetch data from the provided API and push that into database. For the initial setup I am using this command to fetch data. All subsequent process will be handled by backend tasks.

```sh
$ pipenv run python manage.py load_districts_data
$ pipenv run python manage.py fetch_weather_data
```

Run redis using the below command. Ater starting redis, you can check with `redis-cli` followed by `ping` it will return `PONG`.
```sh
$ redis-server
```

Now you can run the below command on different terminals to  `start the development server`, `initate the workers`, `initiate the celery beat` respectively.
```sh
$ pipenv run python manage.py runserver 127.0.0.1:8000
$ pipenv run celery -A core.celery worker --pool=solo -l info
$ pipenv run celery -A core.celery beat -l INFO
```

## APIs

A list of endpoint with description.

| Endpoint | Description |
| -------- | ----------- |
| `http://127.0.0.1:8000/api/v1/coolest-districts/` | lists top 10 coolest districts based on 7 days avg temperature at 2:00PM |
| `http://127.0.0.1:8000/api/v1/travel-suggestions/` | given location, destination and travel_date gives a suggestion whether you should visit the destination or not. |
| `http://127.0.0.1:8000/api/v1/travel-suggestions` | given location, destination and travel_date gives a suggestion whether you should visit the destination or not. |
| `http://127.0.0.1:8000/api/v1/schema/swagger-ui/` | swagger-ui |
| `http://127.0.0.1:8000/api/v1/schema/redoc/` | documentation |
