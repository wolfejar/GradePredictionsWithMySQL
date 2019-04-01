# GradePredictionsWithMySQL  
This is a python web application which uses tensorflow to predict student grades based on mock data from a MySQL database.
It uses Flask as a framework to allow for easy data entry and display of results.

## Dependencies
```bash
pip install tensorflow  
pip install Flask  
pip install matplotlib
```
NOTE: In order to train a new model with TensorFlow, you must have MySQL installed and running on your system. The database required for training this model is available at
https://github.com/wolfejar/SchoolDatabaseMySQL

```bash
pip install mysqlclient
```

## Running the Web App (No MySQL Required)

```bash
python application.py
```

http://127.0.0.1:5000/

## Training a New Model

```bash
python predictor.py [host][user][password][database]
```
