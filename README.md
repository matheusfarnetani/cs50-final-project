# Classpass

![GitHub repo size](https://img.shields.io/github/repo-size/matheusfarnetani/cs50-final-project)
![GitHub language count](https://img.shields.io/github/languages/count/matheusfarnetani/cs50-final-project)
![GitHub forks](https://img.shields.io/github/forks/matheusfarnetani/cs50-final-project)

## The Project
The project is a web app written in Python-Flask called "Classpass".

The bigger idea is, in fact, my college group project. It is an exercise where the premises were to develop a technology solution to an inner college problem.

Basically the solution is to give a RFID card for the people who utilize the inner places, in order to create a more secure space and generate data. This data could serve as a guide for major developments, as it could be analyzed and create insights about the flow of the inner spaces.

The project here, in CS50, was to develop a web app with Flask that could display the data and the graphs that the whole project could create. To be able to do it, I had to study the documentation of  tools such as Flask and its Components, SQLAlchemy and Chart Js. Creating six major routes, being one of them a route with four variants.

## The Routes

![Routes](https://i.imgur.com/s6G9jw4.png)

In this image we have a diagram that illustrates the route's relations. From left to right, the 'root' automatically redirects to '/common/login' that could have two directions, being the first '/common/registers' and the second '/'. Each route was written using Flask's Blueprints concept, so that it was possible to construct a modular base for further development. This project contains 5 blueprints: 

* api: "/api/"
* auth: "/"
* common: "/common"
* graphs: "/graphs"
* tables "/tables"
  
After the authentication process the user is redirected to the auth blueprint, where he can choose between two routes "/graphs" and "/tables". The "/api" and its variants are accessible to the user, but it is not displayed on the screen as its contents are what the JavaScript code fetches to render the "/graphs" and "/tables" pages.

## The Database

The database used in the web app was constructed using SQLAlchemy and later adapted to Flask-SQAlchemy. The content of the database was generated with the database.py file that creates a SQLite3 .db and calls populate.py to generate the random data.

![Database](https://i.imgur.com/6oZWORV.png)

## Files Structure

![Files Structure](https://i.imgur.com/T5Dfa3f.png)

This diagram shows the files structure of the app and each main functionality for the folder.

## Demonstration

In order to complete the final project, you must record a short presetation video.

[Presentation video on youtube](https://www.youtube.com/watch?v=zdunYTcADe0)

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
