# rdf-django
Combine Rdflib with Django.
The goal is to to wrap data tables in to rdf schemas.
The tools to achieve the goal are django, relational databases and rdflib.
The framework enriches data points with semantic namespaces through model and serializer classes. It can be added to any django project and does not necessarily modify the database schema. Mainly it outputs the database content in a defined graph structure. Currently it is only for reading data in rdf/xml.
Http CRUD methods are made with rest_framework.

## Requirements

    Django
    djangorestframework
    rdflib
    django-environ
    django-filter

## Installation

    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

## Api Endpoints

### browsable api:

    http://localhost:8000/api/account/

### json:
    query params: 
    - format=json
    - limit=10
    - search=abc

    GET, POST, PUT, PATCH, DELETE, OPTIONS
    http://localhost:8000/api/account/person/?format=json
    http://localhost:8000/api/account/person/{pk}/?format=json
    http://localhost:8000/api/account/organization/?format=json
    http://localhost:8000/api/account/organization/{pk}/?format=json
    http://localhost:8000/api/account/project/?format=json
    http://localhost:8000/api/account/project/{pk}/?format=json
    http://localhost:8000/api/account/skill/
    http://localhost:8000/api/account/website/

    ... more

### xml:
    query params: 
    - format=xml
    - param=flat (only for person)
    - limit=10
    - search=abc
    - include=person (only for skills)
    
    GET
    http://localhost:8000/api/account/person/?format=xml&param=flat
    http://localhost:8000/api/account/person/{pk}/?format=xml
    http://localhost:8000/api/account/organization/?format=xml
    http://localhost:8000/api/account/organization/{pk}/?format=xml
    http://localhost:8000/api/account/project/?format=xml
    http://localhost:8000/api/account/project/{pk}/?format=xml
    http://localhost:8000/api/account/skill/
    http://localhost:8000/api/account/website/
    
    ... more


## Ontologies

all ontologies are used from :
#### [rdflib](https://rdflib.readthedocs.io/)

## Vizualisation

one tool which I use is:

#### [Protege website](https://protege.stanford.edu/)

#### [GitHub: protege](https://github.com/protegeproject/protege)

    1. run django server
    2. opened the protege GUI
    3. click on:
        File -> open from url 
    4. paste: 
        http://localhost:8000/api/account/person?format=xml

optionally you can add [OntoGraf](https://protegewiki.stanford.edu/wiki/OntoGraf) to show graphical node tree.


## Ressources

[Github: awesome-semantic-web](https://github.com/semantalytics/awesome-semantic-web#contents)

[semantic scholar](https://www.semanticscholar.org/paper/Social-Participation-Network%3A-Linking-Things%2C-and-Piperagkas-Angarita/86c670ef7454d6a4cbaf6a9c0abe72035eff3dae#references)
