import sys
import os
from datetime import datetime, timedelta
import numpy as np
import pickle
import bcrypt
import jwt  # PyJWT for JWT handling
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi import BackgroundTasks
import mlflow
import dagshub
import certifi
from pydantic import BaseModel
from uvicorn import run as app_run
import logging
from src.NetworkSecurity.logging.logger import logger
from src.NetworkSecurity.pipeline.training_pipeline import TrainingPipeline

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# Load environment
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

# MongoDB setup
client = MongoClient(os.getenv("MONGO_DB_URL"), tlsCAFile=certifi.where(), ssl=True)
db = client["PhishingData"]
users_collection = db["Users"]

# App setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dagshub
dagshub.init(repo_owner='adityaav80', repo_name='E2E-Network-Security', mlflow=True)

# Models
class User(BaseModel):
    email: str
    password: str

# Your token validation function
def verify_token_from_header(request: Request):
    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # returns decoded payload with email, role, etc.
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Routes
@app.post("/api/login", tags=["authentication"])
async def login(user: User):
    logger.info(f"User {user.email} attempted login")
    user_db = users_collection.find_one({"email": user.email})

    if not user_db or not bcrypt.checkpw(user.password.encode('utf-8'), user_db['password']):
        logger.exception(f"Login failed for user {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode({
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "role": user_db.get("role", "customer")
    }, SECRET_KEY, algorithm=ALGORITHM)

    logger.info(f"Login successful for {user.email}")
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/signup", tags=["authentication"])
async def signup(user: User):
    if users_collection.find_one({"email": user.email}):
        logger.exception(f"Signup failed - user {user.email} exists")
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({
        "email": user.email,
        "password": hashed_password,
        "role": "customer"
    })

    token = jwt.encode({
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "role": "customer"
    }, SECRET_KEY, algorithm=ALGORITHM)

    logger.info(f"Signup successful for {user.email}")
    return {"success": True, "token": token}

@app.post("/api/train")
async def train_route(request: Request, background_tasks: BackgroundTasks):

    verify_token_from_header(request)

    try:
        auth_header = request.headers.get("Authorization")    
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, options={"verify_signature": False})
        email = decoded.get("sub")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    background_tasks.add_task(run_pipeline_wrapper, email)
    return Response("Training started in background!")


def run_pipeline_wrapper(user_email: str):
    try:
        result = TrainingPipeline().run_pipeline()
        
        send_completion_email(user_email, result)
    except Exception as e:
        logger.exception(e)

def send_completion_email(user_email: str, result):

    if result:
        from_email = os.getenv('MAIL_DEFAULT_SENDER')
        logger.info(f"From Email: {from_email}")
        logger.info(f"To Email: {user_email}")
        
        # Check if both emails are valid
        if not from_email or not user_email:
            logger.error("Invalid email addresses")
            return

        message = Mail(
            from_email=os.getenv('MAIL_DEFAULT_SENDER'),
            to_emails=user_email,
            subject='Training Complete',
            html_content="""
                <h1>Training Complete</h1>
                <p>Your training is complete</p>
            """
        )
        try:
            logger.info(f"About to send mail")

            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            logger.info(f"{response}")
            logger.info(f"SendGrid Response: {response.status_code}, {response.body}, {response.headers}")

        except Exception as e:
            print(str(e))


@app.post("/api/predict")
async def predict_route(request: Request):

    verify_token_from_header(request)

    form_data = await request.form()
    features = {key: float(value) for key, value in form_data.items()}
    values = np.array(list(features.values())).reshape(1, -1)
    logger.info(f"User is trying to predict")

    with open("artifacts/model_trainer/ss.pkl", "rb") as f:
        scaler = pickle.load(f)
    values = scaler.transform(values)
    logger.info(f"Transformed form data to scaled values")

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    try:
        model = mlflow.pyfunc.load_model("models:/Best Model/latest")
        prediction = model.predict(values)
        logger.info(f"Loaded the model for dagshub")
        return JSONResponse(content={"prediction": int(prediction)})
    except Exception as e:
        logger.exception(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=9009, access_log=True)