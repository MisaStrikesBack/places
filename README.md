# Places Exercise Api

This a development exercise

## Contents
* [Staging](#staging)
* [Project setup](#project-setup)
* [Running development stack](#running-the-development-stack)
* [Halting development stack](#halting-development-stack)
* [Testing](#testing)
* [Code Quality](#code-quality)


### Staging

* **Heroku** - https://places-exercise-api.herokuapp.com/

### Developer

| Name  | Contact |
| ------------- | ------------- |
| Misael Ramirez  | misaram89@gmail.com  |

## Development

# Important!: This project WON'T work unless you provide a valid google places api key inside the keys.env file

### Project setup
- Cloning the repo:
```
$ git clone https://github.com/MisaStrikesBack/places.git
```
- Building the docker image using docker-compose
```
$ docker-compose build
```
- Migrating database
```
$ docker-compose run web python manage.py migrate
```
### Running the development stack
- Run in a terminal
```
$ docker-compose up web
```

### Halting development stack
- Run in a terminal
```
$ docker-compose up down
```
- Deleting database volume
```
$ docker-compose up down -v
```

### Testing
- Runing python test suite
```
$ docker-compose run web python manage.py test
```
- Running specific test
```
$ docker-compose run web python manage.py test route.to.test.py
```

### Code Quality
- Running codeclimate
```
$ codeclimate analyze
```
