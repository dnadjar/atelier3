from fastapi import APIRouter, Query, HTTPException
import psycopg2
import os
from dotenv import load_dotenv #
from pydantic import BaseModel, Field
from typing import Optional

# Chargement sécurisé des variables d'environnement
load_dotenv() #

router = APIRouter()

# CORRECTION V4 : Suppression du secret en dur
DB_PASSWORD = os.getenv("DB_PASSWORD") #

# Schéma de validation pour contrer le Mass Assignment (V6)
class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    # Note : 'role' et 'balance' sont exclus (Whitelist) [cite: 207]

def get_db_connection():
    try:
        return psycopg2.connect(
            host="db.neobank.internal",
            database="accounts",
            user="admin",
            password=DB_PASSWORD
        )
    except Exception:
        # CORRECTION V10 : Message générique sans stack trace [cite: 223]
        raise HTTPException(status_code=500, detail="Erreur de connexion sécurisée")

@router.get("/transactions/search")
def search_transactions(user_id: str, keyword: str = Query(..., min_length=1, max_length=50)):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # CORRECTION V1 : Requête paramétrée contre l'injection SQL
        query = "SELECT * FROM transactions WHERE user_id = %s AND description LIKE %s"
        search_pattern = f"%{keyword}%"
        cursor.execute(query, (user_id, search_pattern))
        return {"transactions": cursor.fetchall()}
    except Exception:
        raise HTTPException(status_code=500, detail="Une erreur est survenue lors de la recherche")
    finally:
        if conn:
            conn.close()