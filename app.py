from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
from sqlalchemy import create_engine
import urllib.parse


model = joblib.load("pipeline_pred_Appartement_Paris.pkl")

app = FastAPI(title = "prix appartement Paris API")

password = "L@men@ce2001"
password_enc = urllib.parse.quote_plus(password)
user = "root"
bdd = "immobilier_paris"
host = "localhost"
engine = create_engine(
    f"mysql+pymysql://{user}:{password_enc}@{host}:3306/{bdd}"
)

class Appartement (BaseModel):
    surface_m2	: int
    nombre_pieces : int
    nombre_chambres : int
    etage : int
    ascenseur : int
    balcon : int
    parking : int
    arrondissement : int

@app.post("/predict")
def predict (appartement : Appartement):
    query = f"""
    SELECT prixM2
    FROM arrondissement
    WHERE arrondissement = {appartement.arrondissement}
    """
    prix_m2 = pd.read_sql(query, engine).iloc[0, 0]

    data = pd.DataFrame([appartement.dict()])
    data["prix_m2_moyen_arrondissement"] = prix_m2
    pred = model.predict(data)
    return {"prix_pred" : float(pred[0])}
