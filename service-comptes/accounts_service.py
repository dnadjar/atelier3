from fastapi import APIRouter, Query, HTTPException
import psycopg2
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

# Chargement sécurisé
load_dotenv()

router = APIRouter()
# CORRECTION V4 : On récupère depuis le .env
DB_PASSWORD = os.getenv("DB_PASSWORD")

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def get_db_connection():
    try:
        return psycopg2.connect(
            host="db.neobank.internal",
            database="accounts",
            user="admin",
            password=DB_PASSWORD
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur de connexion sécurisée")

@router.get("/transactions/search")
def search_transactions(user_id: str, keyword: str = Query(..., min_length=1, max_length=50)):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM transactions WHERE user_id = %s AND description LIKE %s"
        search_pattern = f"%{keyword}%"
        cursor.execute(query, (user_id, search_pattern))
        return {"transactions": cursor.fetchall()}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        if conn:
            conn.close()