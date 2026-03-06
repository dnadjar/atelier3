# 🛡️ NeoBank Digital - Audit & Remédiation Sécurité

Ce projet a été réalisé dans le cadre de l'**Atelier n°3 : Sécurisation d'une architecture Cloud**. L'objectif était d'auditer et de corriger une application bancaire (NeoBank) présentant de multiples vulnérabilités critiques.

## 👥 Auteurs
* **Damien Nadjar**
* **Guilliane Dieppois**

---

## 📝 Présentation du Projet
Le projet consiste en une architecture de micro-services comprenant :
1.  **API Gateway (Python/FastAPI)** : Gère l'authentification et l'accès aux comptes.
2.  **Service Comptes (Python/FastAPI)** : Gère la recherche et la consultation de transactions.
3.  **Service Paiements (Node.js/Express)** : Gère les transferts et les profils utilisateurs.

L'ensemble de l'application a été sécurisé pour répondre aux standards de l'industrie (OWASP Top 10) et aux exigences de conformité bancaire.

---

## 🚀 Remédiations Implémentées

### 1. Protection des Données et Injections
* **Correction V1 (Injection SQL)** : Implémentation de requêtes paramétrées pour la recherche de transactions.
* **Correction V5 (XSS Stored)** : Utilisation de `DOMPurify` pour nettoyer les descriptions de transferts.
* **Correction V6 (Mass Assignment)** : Utilisation de schémas Pydantic (Whitelist) pour filtrer les entrées utilisateur lors de la mise à jour de profil.

### 2. Authentification et Contrôle d'Accès
* **Correction V2 (JWT)** : Sécurisation des tokens avec une durée d'expiration (`exp`) de 20 minutes.
* **Correction V3 (IDOR)** : Vérification systématique de la propriété d'un compte avant toute consultation ou action.
* **Correction V7 (Rate Limiting)** : Protection contre le brute-force sur le login (5 tentatives max / 15 min) et limitation globale du trafic.

### 3. Configuration et Infrastructure
* **Correction V4 (Secrets)** : Externalisation complète des secrets (mots de passe DB, clés JWT) via des variables d'environnement (`.env`).
* **Correction V8 (Composants)** : Mise à jour des dépendances Python et Node.js vers des versions exemptes de CVE critiques.
* **Correction V10/V11** : Gestion d'erreurs générique (sans stack trace) et validation du format/poids des requêtes JSON.
* **Correction V12** : Implémentation de `Helmet` (headers de sécurité) et restriction des politiques CORS.

---

## 🛠️ Validation de la Sécurité (DevSecOps)

Le projet intègre une **Pipeline CI/CD** automatisée via GitHub Actions qui effectue les contrôles suivants à chaque push :
* **SCA (Software Composition Analysis)** : Scan des dépendances avec `Safety`.
* **SAST (Static Application Security Testing)** : Analyse du code source avec `Bandit`.
* **Tests Unitaires** : Validation de la logique de sécurité avec `pytest`.



---

## ⚙️ Installation

1.  **Cloner le projet** :
    ```bash
    git clone [https://github.com/dnadjar/atelier3.git](https://github.com/dnadjar/atelier3.git)
    ```
2.  **Configurer les secrets** :
    Copiez le fichier `.env.example` en `.env` et remplissez les variables nécessaires.
3.  **Lancer les tests de sécurité** :
    ```bash
    pytest tests/test_security.py
    ```
