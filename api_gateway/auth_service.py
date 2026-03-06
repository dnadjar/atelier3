from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

router = APIRouter()

# --- CONFIGURATION (Phase 3 anticipée) ---
SECRET_KEY = os.getenv("JWT_SECRET", "n3ob@nk_super_secret_key_2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20  # Correction V2 : Expiration courte


# --- FONCTIONS UTILITAIRES ---

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def check_account_ownership(user_id: str, account_id: str):
    # Simulation d'une vérification en base de données
    # Dans la réalité, on vérifierait si cet account_id appartient bien à ce user_id
    db_mock = {"123": ["ACC-001", "ACC-002"], "456": ["ACC-999"]}
    return account_id in db_mock.get(user_id, [])


# --- ROUTES ---

@router.post("/login")
def login(username: str, password: str):
    # Simulation d'auth (V10 : message générique)
    if username == "admin" and password == "secure_password":
        return {"access_token": create_access_token({"user_id": "123", "role": "admin"})}

    raise HTTPException(status_code=401, detail="Identifiants invalides")


@router.get("/account/{account_id}")
def get_account(account_id: str, token: str):
    try:
        # 1. Décodage et vérification de l'expiration (V2)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_from_token = payload.get("user_id")

        # 2. CORRECTION V3 (IDOR) : Vérification de propriété
        if not check_account_ownership(user_id_from_token, account_id):
            # V9 : On devrait loguer cet incident (Phase 3)
            raise HTTPException(status_code=403, detail="Accès refusé : vous n'êtes pas le propriétaire de ce compte")

        return {"account_id": account_id, "balance": 1500.0, "currency": "EUR"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expirée, veuillez vous reconnecter")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")