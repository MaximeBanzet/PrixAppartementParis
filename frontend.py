import streamlit as st
import requests

st.title("Prédiction Prix Appartement")

# Inputs utilisateur
surface = st.number_input("Surface (m²)", min_value=10, max_value=1000, value=50)
pieces = st.number_input("Nombre de pieces", min_value=1, max_value=10, value=2)
chambres = st.number_input("Nombre de chambres", min_value=1, max_value=10, value=2)
etage = st.number_input("Etage", min_value=0, max_value=10, value=5)
ascenseur = st.number_input("Il y a t'il un ascenseur", min_value=0, max_value=1, value=0)
balcon = st.number_input("Il y a t'il un balcon", min_value=0, max_value=1, value=0)
parking = st.number_input("Il y a t'il un parking", min_value=0, max_value=1, value=0)
arrondissement = st.number_input("Quel arrondissiment", min_value=1, max_value=20, value=17)

if st.button("Prédire le prix"):
    # Créer la requête JSON
    data = {
        "surface_m2": surface,
        "nombre_pieces" : pieces,
        "nombre_chambres": chambres,
        "etage" : etage,
        "ascenseur" : ascenseur,
        "balcon" : balcon,
        "parking" : parking,
        "arrondissement" : arrondissement
    }

    # Appeler FastAPI
    response = requests.post("http://127.0.0.1:8000/predict", json=data)
    
    if response.status_code == 200:
        prix = response.json()["prix_pred"]
        st.success(f"Prix estimé : {prix:.2f} €")
    else:
        st.error("Erreur lors de la prédiction")