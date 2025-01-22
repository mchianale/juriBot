#!/bin/bash
# encoderAPI
echo "--------------------------------------------------"
echo "build and push images of each services"
echo "--------------------------------------------------"

echo "🔨 Building the Docker image for the encoderAPI..."
docker build -f ./encoderAPI/Dockerfile.encoderAPI -t mchianale/encoder-api:latest .
echo "📤 Pushing the Docker image to Docker Hub..."
docker push mchianale/encoder-api:latest

echo "🔨 Building the Docker image for the vectorSimilarityAPI..."
docker build -f ./vectorSimilarityAPI/Dockerfile.vectorSimilarityAPI -t mchianale/vector-similarity-api:latest .
echo "📤 Pushing the Docker image to Docker Hub..."
docker push mchianale/vector-similarity-api:latest

echo "🔨 Building the Docker image for the juriBot..."
docker build -f ./juriBot/Dockerfile.juriBot -t mchianale/juribot-api:latest .
echo "📤 Pushing the Docker image to Docker Hub..."
docker push mchianale/juribot-api:latest

echo "--------------------------------------------------"

