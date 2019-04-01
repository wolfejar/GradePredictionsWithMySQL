# GradePredictionsWithMySQL  
This is a python web application which uses tensorflow to predict student grades based on mock data from a MySQL database.
It uses Flask as a framework to allow for easy data entry and display of results.

## Dependencies
```bash
pip install tensorflow  
pip install Flask  
pip install matplotlib
```
NOTE: You must have MySQL installed and runnnig on your system. The database required for training this model will be uploaded
soon.

```bash
pip install mysqlclient
```

## Training a New Model

```bash
python predictor.py [host][user][password][database]
```

## Running the Web App (No MySQL Required)

```bash
python predictor.py
```

http://127.0.0.1:5000/
