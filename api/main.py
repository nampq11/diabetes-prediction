import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from loguru import logger 
from pydantic import BaseModel

app = FastAPI()

class Diabetes_measures(BaseModel):
    Pregnancies: int = 6 # Number of times pregnant 
    Glucose: int = (
        148 # Plasma glucose concentration a 2 hours in an oral glucose tolerance test
    )
    BloodPressure: int = 72 # Diastolic blood pressure (mm Hg)
    SkinThickness: int = 35 # Triceps skin fold thickness (mm)
    Insulin: int = 0 # 2-Hour serum insulin
    BMI: float = 33.6 # Body mass index
    DiabetesPedigreeFunction: float = 0.627
    Age: int = 50 # Age (years)

model = joblib.load('./models/model.pkl')

@app.get("/")
def check_health():
    return {"Status": "Hello World!"}

cache = {}

@app.post("/predict")
def predict(data: Diabetes_measures):
    logger.info('Making predictions...')
    logger.info(data)
    logger.info(jsonable_encoder(data))
    logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
    result = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]

    return {'result':  ['Normal', 'Diabetes'][result]}

@app.post("/predict_cache")
def predict_cache(data: Diabetes_measures):
    if (str(data)) in cache:
        logger.info("Getting result from cache!")
        return cache[str(data)]
    else:
        logger.info('Making preidictions...')
        logger.info(data)
        logger.info(jsonable_encoder(data))
        logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
        result = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]
        cache[str(data)] = ["Normal", "Diabetes"][result]

        return {"result": ['Normal', "Diabetes"][result]}