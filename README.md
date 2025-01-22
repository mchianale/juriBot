# RAG pour le Droit Français - Code de l'Éducation

Ce projet vise à créer un **Agent RAG** (Retrieval-Augmented Generation) pour le droit français, spécifiquement pour le **Code de l'Éducation**. L'objectif est de développer un agent conversationnel capable de répondre à des questions sur les articles en vigueur du Code de l'Éducation, en accédant directement aux textes officiels sur [Légifrance](https://www.legifrance.gouv.fr).

Le projet se compose de trois services principaux :

1. **API d'Embedding** : Utilisation de **sentence-transformers** avec le modèle `paraphrase-multilingual-mpnet-base-v2` pour transformer les articles du Code de l'Éducation en embeddings, facilitant ainsi leur comparaison par similarité.
   
2. **API ChromaDB** : Stockage et gestion des embeddings dans **ChromaDB**, permettant de faire des requêtes basées sur la similarité pour extraire les articles les plus pertinents en réponse aux questions de l'utilisateur.

3. **API RAG** : Cette API représente l'agent **Mistral**, qui utilise les services précédents pour répondre aux questions des utilisateurs en récupérant les articles les plus pertinents, générant ainsi des réponses contextuelles et précises.

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
0. Creer la clé Mistral
```bash
cd juriBot
touch .env
echo "MISTRAL_API_KEY=your-api-key-here" >> .env
```

1. Clonez ce dépôt : 
```bash
git clone https://github.com/your-username/nom-du-repository.git
```

2. Installez les dépendances : 
```bash
pip install -r requirements.txt
```

3. Uilisation Rapide avec docker-compose
```bash
docker-compose up --build -d
```
**Warning** : Avant de faire des requêtes sur les différents services, attendre qu'ils tournent tous.

4. Lancer StreamLit
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


