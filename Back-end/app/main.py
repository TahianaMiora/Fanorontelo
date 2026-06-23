# app/main.py
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Gestion sécurisée du chemin pour les modules locaux
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.routes import router as api_router

app = FastAPI(title="Fanoron-telo API - ISPM Hackathon")

# Configuration CORS pour que le pôle Frontend puisse se connecter sans blocage navigateur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pour y aller plus vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes du jeu
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    # Lancement du serveur sur le port 8000
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)