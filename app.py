import sys
import os
import certifi
import pymongo
import pandas as pd

from dotenv import load_dotenv
load_dotenv()   # ✅ IMPORTANT

# ================= ENV CONFIG =================
ca = certifi.where()

mongo_db_url = os.getenv("MONGODB_URL")
print("MongoDB URL Loaded:", mongo_db_url)

if mongo_db_url is None:
    raise Exception("❌ MONGODB_URL not found in .env file")

# ================= PROJECT IMPORTS =================
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME
)

# ================= DATABASE =================
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# ================= FASTAPI =================
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")

# ================= ROUTES =================
@app.get("/")
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        # 🔥 LAZY IMPORT (VERY IMPORTANT FIX)
        from networksecurity.pipeline.training_pipeline import TrainingPipeline

        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("✅ Training completed successfully")

    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=model
        )

        y_pred = network_model.predict(df)
        df["prediction"] = y_pred

        df.to_csv("prediction_output/output.csv", index=False)

        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse(
            "table.html",
            {"request": request, "table": table_html}
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)

# ================= MAIN =================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
