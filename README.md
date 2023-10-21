# Coolest Districts API
- [Data Source](https://open-meteo.com/en/docs)
- API for the coolest 10 districts based on the average temperature at 2pm for the next 7 days.
- API where given location, destination, and the date of travel. A decision is given whether to travel or not based on the temperature of 2pm of both places.

## Dependencies
There is a few dependencies which are required to make the application work correctly:
| package / database | Version |
| ------ | ------ |
| python | 3.11 |
| django | 4.2.6 |
| djangorestframework | 3.14.0 |
| mysqlclient | 2.2.0 |
| python-dotenv | 1.0.0 |
| requests | 2.31.0 |
| drf-spectacular | 0.26.5 |
| locust | 2.17.0 |
| MySQL DB | 8.0.31 |

-- As the application does not require complex database writes. I decided to go with mySQL database as mySQL is good for data reads.

## Installation
requires [python](https://www.python.org/) 3.11 & pipenv to run

-First install the pipenv package with the below command
```sh
$ pip install pipenv
```
-Install the dependency packages using the below command from pipfile.
```sh
$ pipenv install
```

## Running the Project

-First you need to configure the dotenv file. I have provided the .env_example file. Rename it to .env and put the required parameters.
-Once the dotenv file has been configured please execute the below command to migrate the Database.
```sh
$ pipenv run python manage.py migrate
```

-After that to load the initial data execute the below commands.
- first command will parse the `districts.json` file and push the districts data into the database.
- second command will use the districts longitude and latitude data, fetch data from the provided API and push that into database. In real scenario we could have pull data and updated the data every few hours. I have not implemented that here.

```sh
$ pipenv run python manage.py load_districts_data
$ pipenv run python manage.py fetch_weather_data
```

-Now you can run the development server using the below command.
```sh
$ pipenv run python manage.py runserver 127.0.0.1:8000
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
