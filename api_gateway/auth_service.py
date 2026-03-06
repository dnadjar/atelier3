from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement (V4)
load_dotenv()

router = APIRouter()

# --- CONFIGURATION SÉCURISÉE ---
SECRET_KEY = os.getenv("JWT_SECRET", "fallback_key_for_dev_only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20  # Correction V2 : Expiration courte

# Récupération des identifiants depuis l'environnement (V4)
# On ne met plus aucune valeur par défaut en dur ici
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# --- FONCTIONS UTILITAIRES ---

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def check_account_ownership(user_id: str, account_id: str):
    # Simulation de vérification de propriété (V3)
    db_mock = {"123": ["ACC-001", "ACC-002"], "456": ["ACC-999"]}
    return account_id in db_mock.get(user_id, [])

# --- ROUTES ---

@router.post("/login")
def login(username: str, password: str):
    # CORRECTION V4 : On compare avec les variables chargées depuis le .env
    # Bandit ne verra plus la chaîne de caractères "secure_password"
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"access_token": create_access_token({"user_id": "123", "role": "admin"})}

    # V10 : Message d'erreur générique
    raise HTTPException(status_code=401, detail="Identifiants invalides")

@router.get("/account/{account_id}")
def get_account(account_id: str, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_from_token = payload.get("user_id")

        if not check_account_ownership(user_id_from_token, account_id):
            raise HTTPException(status_code=403, detail="Accès refusé")

        return {"account_id": account_id, "balance": 1500.0, "currency": "EUR"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expirée")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")