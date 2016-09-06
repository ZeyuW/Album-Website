# Album-Website
### For detailed video demo, visit my homepage: http://www-personal.umich.edu/~simplee


## Run website on localhost:
### Create vagrant environment and run virtual machine
- vagrant up
- vagrant ssh
- cd /vagrant
- source venv/bin/activate

### Create database: 485p3 and load data (implement tbl_create.sql and load_data.sql in sql/)
- mysql: create database 485p3
- sh local_mkdb.sh

## Run the website
- python local_app.python

## Visit: localhost:3000/b5340568bdcd46b4b5be/pa3
