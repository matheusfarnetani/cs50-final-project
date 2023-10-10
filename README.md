# Classpass

![GitHub repo size](https://img.shields.io/github/repo-size/matheusfarnetani/cs50-final-project)
![GitHub language count](https://img.shields.io/github/languages/count/matheusfarnetani/cs50-final-project)
![GitHub forks](https://img.shields.io/github/forks/matheusfarnetani/cs50-final-project)

## Description
[Presentation video on youtube](https://www.youtube.com/watch?v=zdunYTcADe0)

The classpass web app is a tool to access data from a RFID card systems. Made with Flask, SQLAlchemy and Chart.js it displays the data as tables and graphs to the user.

## Requirements

Before starting, please confirm that you have:

* `Python 3.10.12`
* Knowlegde of how to create python `virtual environments`. See (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

## Running

Follow this steps to run `Classpass`.

### Activate your virtual enviroment

Linux and macOS
```
source env/bin/activate
```
Windows
```
.\env\Scripts\activate
```

### Install requirements
```
pip install -r requirements.txt
```

### Run Flask
Export `FLASK_APP` enviroment variable
```
export FLASK_APP=classpass
```

Run `flask run`
```
flask run
```

## How to register
In order to create an account and log in the app, you need to provide a type and uid of your card. Choose one of the three options:
* If you want use `student`, the card uid should be `AA AA AA AB`
* If you want use `collaborator`, the card uid should be `CA CA AA BB`
* If you want use `visitant`, the card uid should be `CC CC CC CB`

## Routes
![Routes](https://i.imgur.com/s6G9jw4.png)

## Database
![Database](https://i.imgur.com/6oZWORV.png)

## Files Structure
![Files Structure](https://i.imgur.com/T5Dfa3f.png)
