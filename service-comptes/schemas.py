from pydantic import BaseModel, Field, validator
import re

# Schéma pour la recherche (V1)
class SearchQuery(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=50) # Type strict [cite: 195]

# Schéma pour la mise à jour du profil (Correction V6 : Mass Assignment) [cite: 35, 205, 207]
class UserProfileUpdate(BaseModel):
    # On ne met que les champs autorisés (Whitelist) [cite: 207]
    first_name: str = Field(None, max_length=50)
    last_name: str = Field(None, max_length=50)
    email: str = Field(None, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    # On exclut 'role' ou 'balance' ici pour empêcher un utilisateur de se promouvoir admin [cite: 113, 207]