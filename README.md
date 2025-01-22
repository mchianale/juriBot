# RAG pour le Droit Français - Code de l'Éducation

Ce projet vise à créer un **Agent RAG** (Retrieval-Augmented Generation) pour le droit français, spécifiquement pour le **Code de l'Éducation**. L'objectif est de développer un agent conversationnel capable de répondre à des questions sur les articles en vigueur du Code de l'Éducation, en accédant directement aux textes officiels sur [Légifrance](https://www.legifrance.gouv.fr).

## Sommaire

- [Introduction](#introduction)
  - [EncoderAPI](#introduction)
  - [ChromaAPI](#introduction)
  - [JuriBot API](#introduction)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
  - [Clonage du Dépôt](#clonez-ce-dépôt)
  - [Création de la Clé Mistral](#creer-la-clé-mistral)
  - [Installation des Dépendances](#installez-les-dépendances)
  - [Utilisation avec Docker Compose](#uilisation-rapide-avec-docker-compose)
  - [Lancement de Streamlit](#lancer-streamlit)
- [Documentation et Accès](#documentation-et-accès)
- [Données](#les-données)
  - [LegiFrance](#legifrance)
  - [Chroma DB](#chroma-db---vector-database)
- [Kubernetes](#kubernetes)
  - [Build et Push des Images Docker](#build-and-push-services-images-vers-dockerhub)
  - [Déploiement Kubernetes](#deploiement-avec-kubernetes)
  - [Exécution Locale avec Kubernetes](#tourner-en-local-avec-kubernetes)

---

## Introduction
**Le projet se compose de trois services principaux :**

1. **EncoderAPI** :
   - Utilisation de **sentence-transformers** avec le modèle `paraphrase-multilingual-mpnet-base-v2` pour transformer les articles du Code de l'Éducation en embeddings, facilitant ainsi leur comparaison par similarité.

2. **ChromaAPI** :
   - Gère la base de données vectorielle (ajout, modification, suppression de documents).
   - Traite les requêtes pour obtenir les top_k voisins les plus proches.
   - Fait appel à EncoderAPI pour obtenir les embeddings des textes.

3. **JuriBot API** :
   - Crée un agent (suivant la documentation de Mistral) utilisant un LLM pour répondre aux requêtes des utilisateurs, mais également pour gérer des outils.
   - Utilise un System Prompt pour rendre les réponses du LLM plus pertinentes.
   - Ici, un seul outil est utilisé : il consiste à récupérer les top_k voisins les plus proches d’une requête utilisateur (que le LLM peut adapter).
   - Fournit un point d’API pour interagir avec JuriBot (gère également l’historique des messages).

Une démonstration de l'agent conversationnel est disponible via **Streamlit** (en local), permettant aux utilisateurs de tester l'agent avec une interface.
    
---

## Fonctionnalités

- **Recherche de textes législatifs** : Interrogez le Code de l'Éducation pour obtenir les articles les plus pertinents en fonction des demandes.
- **Précision et pertinence** : Grâce à l'intégration de **ChromaDB** et des embeddings, l'agent fournit des réponses précises basées sur la similarité des articles.
- **Interface conviviale** : Testez facilement l'agent via **Streamlit** pour une expérience utilisateur fluide.

---

## Prerequis 
- python >= `3.10`
- une clé mistral API
- Docker

---

## Installation
### Clonez ce dépôt : 
```bash
git clone https://github.com/your-username/nom-du-repository.git
```

### Creer la clé Mistral
```bash
cd juriBot
touch .env
echo "MISTRAL_API_KEY=your-api-key-here" >> .env
```

### Installez les dépendances : 
```bash
pip install -r requirements.txt
```

### Uilisation Rapide avec docker-compose
```bash
docker-compose up --build -d
```
**Warning** : Avant de faire des requêtes sur les différents services, attendre qu'ils tournent tous.

### Lancer StreamLit
```bash
streamlit run streamLitFront/app.py
```

---

## Documentation et accès 
- **encoderAPI** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **vectorSimilarityAPI** : [http://localhost:8001/docs](http://localhost:8001/docs)
- **juriBot** : [http://localhost:8002/docs](http://localhost:8002/docs)

---

# Les données 

## LegiFrance
- Environ `5000` articles du Code de l’éducation (voir  [Légifrance](https://www.legifrance.gouv.fr)).
- Les textes des articles sont vectorisés.
- Les métadonnées sont également conservées (section de l’article, partie législative ou réglementaire).

## CHROMA DB - Vector Database
- Par défaut, utilise la distance cosinus.
- Réduit l’espace de recherche en utilisant l’ANN - les recherches approximatives de voisins les plus proches.

---

# Kubernetes 
## Build and Push Services Images vers DockerHub
```bash
bash buildAndPush.sh
```
**Warning** : changer le username, ici `mchianale`

## Deploiement avec kubernetes
```bash
minikube delete # Remettre a niveau le cluster
minikube start
# encoderAPI
kubectl apply -f kube/encoderAPI-service-deployment.yml
# vectorSimilarityAPI
kubectl apply -f kube/vectorSimilarityAPi-service-deployment.yml
# juryBot
kubectl apply -f kube/juriBot-service-deployment.yml
```

## Tourner en local avec kubernetes

```bash
Start-Process kubectl -ArgumentList 'port-forward', 'service/encoder-api', '8000:8000'
Start-Process kubectl -ArgumentList 'port-forward', 'service/vector-similarity-api', '8001:8001'
Start-Process kubectl -ArgumentList 'port-forward', 'service/juribot-api', '8002:8002'
```
**Warning** : bien verifieer que les status de chaque pods soient en `Running`:

```bash
kubectl get pods
```


