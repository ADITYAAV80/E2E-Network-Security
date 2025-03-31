import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")


from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logger
from src.NetworkSecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
import numpy as np
import mlflow
import pickle

# FastAPI app setup
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(" Training completed successfully!")
    except Exception as e:
        logger.exception(e)
        raise NetworkSecurityException(e, sys)
    
@app.get("/predict")
async def take_input(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})


def predict(features: dict):

    return features

@app.post("/predict")
async def predict_route(request: Request):
    
    form_data = await request.form()

    # Convert form data to a dictionary with key-value pairs
    features = {key: float(value) for key, value in form_data.items()}
    # Pass the extracted features to the model's prediction function

    values = np.array(list(features.values())).reshape(1,-1)

    with open("artifacts/model_trainer/ss.pkl","rb") as f:
        scaler = pickle.load(f)

    values = scaler.transform(values)
    
    # MLflow settings (update these with your settings)
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")  
    model_name = "Best Model"

    # Load model from MLflow
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    try:
        # Option 1: Load the latest production model
        model = mlflow.pyfunc.load_model(f"models:/{model_name}/latest")
        
        # Make prediction
        prediction = model.predict(values)
        
        return {"prediction": int(prediction)}
    
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
