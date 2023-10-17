# CookingCrafts food cooking helper
## _Fresh and tasty app which helps you create your own cooking masterpiece_
## Available at: https://cookingcrafts.b2k.me/recipes
## based on:
[![N|Solid](https://static.djangoproject.com/img/logos/django-logo-negative.svg)](https://www.djangoproject.com/)
## and
[![N|Solid](https://www.django-rest-framework.org/img/logo.png)](https://www.django-rest-framework.org/)
## and also on:
[![N|Solid](https://logos-download.com/wp-content/uploads/2016/09/React_logo_wordmark.png)](https://react.dev/)
## with PostgreSQL as database provider:
[![N|Solid](https://wiki.postgresql.org/images/a/a4/PostgreSQL_logo.3colors.svg)](https://www.postgresql.org/)
## and with power of:
[![N|Solid](https://www.docker.com/wp-content/uploads/2023/08/logo-guide-space-1.svg)](https://www.docker.com/)
  
## Features
Contains SPA frontend page + backend API module, which are interconnected using json exchange of data.

- You can create your recipe with image and detailed information of cooking process
- Available database of ingredients (more than 2000)
- Recipe can be marked using tag for easy searching in future
- Recipes could be put in favourites, also authors could be subscribed
- Availability to put recipe into shopping list to ease the final process of creating and downloading shopping list
- Recepies can have more than one tag simultaneously 

## Tech

CookingCrafts uses a number of open source and proprietary projects to work properly:

- [Python] - Python 3.9
- [Django] - Web framework to rule them all!
- [Django Rest Framework (DRF)] - REST API support for Django
- [React] - Frontend framework to user is working with
- [PostgreSQL] - Most powerful Open Source Database
- [Docker] - Docker and docker hub for images and container management
- [GitHub Actions] - Service for realisation CI/CD

And of course Coookingcrafts itself is open source with a [public repository][git-repo-url] on [GitHub][Rexant-b2k].

## API
Api documantation is available at https://cookingcrafts.b2k.me/api/docs/
Contains all request and expected responses from backend
Root API Endpoint is located at https://cookingcrafts.b2k.me/api/

## Installation
No installation is required. Server already available on: https://cookingcrafts.b2k.me/

### Local usage
### if you want to install copy of this server for local usage:
##### Install the dependencies and devDependencies and start the server (Linux/MacOS example).

```sh
cd backend
python -m venv venv
python -m pip install --upgrade pip
source venv/bin/activate
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs 
```

For production environments (automatic)...

```sh
pip install -r backend/requirements.txt
cd frontend
npm i
```

##### Making migrations
```sh
python manage.py migrate
```

##### Running server
```sh
python backend/manage.py runserver
cd frontend
npm run start
```

## Plugins

Kittygram is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin       | README          |
| -------------| --------------- |
| Dillinger    | [Dillinger.io]  |
|GitHub Actions| [GitHub Actions]|

## Docker
The script for automatic deploy is located in **.github/workflows/main.yml** file. This script maintain automatic checking of PEP8 code-style, and deploy on author docker account and then - to the production server. The project is available on **https://CookingCrafts.b2k.me/**. You are able to fork the repository, alter account and images name, provide your secrets to access to the DockerHub and production server.

## Plugins

Kittygram is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin       | README          |
| -------------| --------------- |
| Dillinger    | [Dillinger.io]  |
|GitHub Actions| [GitHub Actions]


## Authors
The team of [Yandex LLC](https://yandex.com) (frontend of product),
[Sergei Baryshevskii](https://www.linkedin.com/in/barysecho/) (backend, database settings and migrations, API, endpotints, docker and github workflow instructions (CI/CD))

## License

BSD-3 Clause License

**Free Software, Hello everybody**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Rexant-b2k]: <https://github.com/Rexant-b2k>
   [git-repo-url]: <https://github.com/Rexant-b2k/CookingCrafts.git>
   [Django]: <https://www.djangoproject.com>
   [Python]: <https://www.python.org/>
   [Django Rest Framework (DRF)]: <https://www.django-rest-framework.org/>
   [Dillinger.io]: <https://dillinger.io/>
   [React]: <https://react.dev/>
   [Docker]: <https://www.docker.com/>
   [GitHub Actions]: <https://github.com/features/actions>
   [PostgreSQL]: <https://www.postgresql.org/>