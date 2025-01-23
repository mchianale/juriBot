# RAG pour le Droit Français - Code de l'Éducation

Ce projet vise à créer un **Agent RAG** (**Retrieval-Augmented Generation**) pour le droit français, spécifiquement pour le **Code de l'Éducation**. L'objectif est de développer un agent conversationnel capable de répondre à des questions sur les articles en vigueur du Code de l'Éducation, en accédant directement aux textes officiels sur [Légifrance](https://www.legifrance.gouv.fr).

## Powered by

<p align="center">
  <img src="https://avatars.githubusercontent.com/u/132372032?s=200&v=4" style="height:28px; vertical-align:middle;" alt="Mistral AI" />
  <img src="https://img.shields.io/badge/-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/-ChromaDb-5E17EB?style=for-the-badge&logo=code&logoColor=white" alt="ChromaDb" />
  <img src="https://img.shields.io/badge/-HuggingFace-FFAE42?style=for-the-badge&logo=huggingface&logoColor=white" alt="HuggingFace" />
</p>

---

## Sommaire

- [Introduction](#introduction)
  - [EncoderAPI](#introduction)
  - [ChromaAPI](#introduction)
  - [JuriBot API](#introduction)
- [Données](#les-données)
  - [LegiFrance](#legifrance)
  - [Chroma DB](#chroma-db---vector-database)
- [Réutilisation](#réutilisation)
- [Source](#source)

---

## Introduction
![architecture](https://github.com/mchianale/juribot/blob/main/img/architecture.png)

**Le projet se compose de trois services principaux :**

1. **EncoderAPI** :
   - Utilisation de `sentence-transformers` avec le modèle `dangvantuan/french-document-embedding` pour transformer les articles du Code de l'Éducation en embeddings, facilitant ainsi leur comparaison par similarité.

2. **ChromaAPI** :
   - Gère la base de données vectorielle (ajout, modification, suppression de documents).
   - Traite les requêtes pour obtenir **les top_k voisins les plus proches**.
   - Fait appel à EncoderAPI pour obtenir les embeddings des textes.

3. **JuriBot API** :
   - Crée un agent (suivant la documentation de `Mistral`) utilisant un LLM pour répondre aux requêtes des utilisateurs, mais également pour gérer des outils.
   - Utilise un System Prompt pour rendre les réponses du LLM plus pertinentes.
   - Ici, un seul outil est utilisé : il consiste à récupérer les top_k voisins les plus proches d’une requête utilisateur (que le LLM peut adapter).
   - Fournit un point d’API pour interagir avec JuriBot (gère également l’historique des messages).

Une démonstration de l'agent conversationnel est disponible via `Streamlit` (en local), permettant aux utilisateurs de tester l'agent avec une interface.
    
---

## Fonctionnalités

- **Recherche de textes législatifs** : Interrogez le Code de l'Éducation pour obtenir les articles les plus pertinents en fonction des demandes.
- **Précision et pertinence** : Grâce à l'intégration de **ChromaDB** et des embeddings, l'agent fournit des réponses précises basées sur la similarité des articles.
- **Interface conviviale** : Testez facilement l'agent via **Streamlit** pour une expérience utilisateur fluide.

---

## Documentation et accès 
- **encoderAPI** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **vectorSimilarityAPI** : [http://localhost:8001/docs](http://localhost:8001/docs)
- **juriBot** : [http://localhost:8002/docs](http://localhost:8002/docs)

---

# Les données 

## LegiFrance
- Voir [mchianale/RAG_droitFr](https://github.com/mchianale/RAG_droitFr) pour la récupération des données en `json`.
- Environ `5000` articles du Code de l’éducation (voir  [Légifrance](https://www.legifrance.gouv.fr)).
- Les textes des articles sont vectorisés.
- Les métadonnées sont également conservées (section de l’article, partie législative ou réglementaire).

## CHROMA DB - Vector Database
- Par défaut, utilise la distance cosinus.
- Réduit l’espace de recherche en utilisant l’ANN - les recherches approximatives de voisins les plus proches.

## Modèle pour les embeddings
- Choix du modèle `dangvantuan/french-document-embedding` : **305M** de paramètres voir [dangvantuan/french-document-embedding](https://huggingface.co/dangvantuan/french-document-embedding)
- Le choix du modèle s'est fait grâce au benchmark proposé ici : [MTEB: Massive Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard)

---

## Réutilisation
- Projet réutilisable avec `docker-compose` ou `kubernetes`.
- **Voir [les instructions](https://github.com/mchianale/juribot/edit/main/RUN.md)**  

---

## Source

- [**ChromaDB**](https://www.trychroma.com/)
- [**LegiFrance**](https://www.legifrance.gouv.fr/)
- [**mchianale/RAG_droitFr**](https://github.com/mchianale/RAG_droitFr)
- [**MTEB: Massive Text Embedding Benchmark**](https://arxiv.org/pdf/2210.07316)
- [**Mistral documentation**](https://docs.mistral.ai/)
