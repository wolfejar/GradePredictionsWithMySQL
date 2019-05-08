# GradePredictionsWithSQLServer  
This is a python web application which uses tensorflow to predict student grades based on mock data from a SQLServer database.
It uses Flask as a framework to allow for easy data entry and display of results.

## Dependencies
```bash
pip install tensorflow  
pip install Flask 
pip install flask_bootstrap
pip install matplotlib
pip install pandas
pip install Cython
pip install pymssql
```

NOTE: You must have Microsoft SQL Server running on your system. The database required for training this model is available at
https://github.com/wolfejar/SchoolDatabaseSQLServer  

### Running on MacOS  

Instructions to run SQL Server with docker: https://adamwilbert.com/blog/2018/3/26/get-started-with-sql-server-on-macos-complete-with-a-native-gui  

```bash
brew install unixodbc
brew install freetds
```

## Running the Web App

```bash
python application.py [host][user][password][database]
```

http://127.0.0.1:5000/

## Training a New Model

```bash
python predictor.py [host][user][password][database]
```
