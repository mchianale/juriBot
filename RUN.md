# RAG pour le Droit Français - Code de l'Éducation - Réutilisation

## Sommaire

- [Installation](#installation)
  - [Prérequis](#prérequis)
  - [Clonage du Dépôt](#clonez-ce-dépôt)
  - [Création de la Clé Mistral](#creer-la-clé-mistral)
  - [Installation des Dépendances](#installez-les-dépendances)
  - [Utilisation avec Docker Compose](#uilisation-rapide-avec-docker-compose)
  - [Lancement de Streamlit](#lancer-streamlit)
- [Kubernetes](#kubernetes)
  - [Build et Push des Images Docker](#build-and-push-services-images-vers-dockerhub)
  - [Déploiement Kubernetes](#deploiement-avec-kubernetes)
  - [Exécution Locale avec Kubernetes](#tourner-en-local-avec-kubernetes)

---

## Installation
### Prérequis 
- python >= `3.10`
- une clé mistral API
- Docker
  
### Clonez ce dépôt : 
```bash
git clone https://github.com/your-username/nom-du-repository.git
```

### Créer la clé Mistral
```bash
cd juriBot
touch .env
echo "MISTRAL_API_KEY=your-api-key-here" >> .env
```

### Installez les dépendances
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


