# Encoder API  

**Objectif** : Fournir des embeddings à partir de documents textuels en utilisant un modèle pré-entraîné. Cette API est conçue pour faciliter l'encodage rapide et efficace de textes dans un espace vectoriel.  

---

## Configuration du modèle  

Le modèle utilisé pour générer les embeddings est configurable via le fichier `model_config.json`, situé dans le dossier `encoderAPI`.  

### Configuration du modèle :  

- **`model_name`** : Nom du modèle utilisé pour générer les embeddings. Par défaut, `dangvantuan/french-document-embedding`.  
- **`trust_remote_code`** : Indique si le code distant du modèle doit être approuvé. Si activé (`true`), n'utilisez que des modèles fiables.  

---

## Endpoints  

### 1. **Vérification de santé**  
- **Route** : `GET /health_check`  
- **Tags** : Monitoring  
- **Paramètres d'entrée** : Aucun  
- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Message indiquant le résultat du test de santé.  

---

### 2. **Créer des embeddings**  
- **Route** : `GET /encode`  
- **Tags** : Encodage  
- **Paramètres d'entrée** :  

| Nom         | Type          | Obligatoire | Description                                    |
|-------------|---------------|-------------|------------------------------------------------|
| `documents` | `array[string]` | Oui         | Liste de chaînes de caractères à encoder.     |

- **Champs de sortie** :  

| Champ         | Type              | Description                                       |
|---------------|-------------------|---------------------------------------------------|
| `status`      | `string`          | Statut de l'exécution (`success` ou `failure`).   |
| `embeddings`  | `array[array]`    | Liste des embeddings générés pour chaque document. |

---

## Tags  

- **Monitoring** : Regroupe les endpoints utilisés pour vérifier la santé et la disponibilité de l'API.  
- **Encodage** : Regroupe les endpoints permettant de générer des embeddings.  
