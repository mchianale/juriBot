# VectorSimilarity API  

**Objectif** : Fournir une interface pour gérer une base de données vectorielle (ChromaDB), permettant des recherches par similarité, l'ajout, la mise à jour et la suppression de documents.  

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

### 2. **Requête par similarité**  
- **Route** : `GET /query`  
- **Tags** : Querying  
- **Paramètres d'entrée** :  

| Nom        | Type          | Obligatoire | Description                                       |
|------------|---------------|-------------|---------------------------------------------------|
| `query`    | `string`      | Oui         | Texte de la requête.                             |
| `n_results`| `integer`     | Oui ou Default  | Nombre maximal de résultats à retourner.         |
| `include`  | `array[string]` | Oui ou Default      | Informations incluses (`ids`, `documents`, `metadatas`, `distances`, etc.). |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `results` : Résultats des documents les plus pertinents.  

---

### 3. **Ajouter un document**  
- **Route** : `POST /add_one_document`  
- **Tags** : Manage one document  
- **Paramètres d'entrée** :  

| Nom        | Type       | Obligatoire | Description                         |
|------------|------------|-------------|-------------------------------------|
| `document` | `string`   | Oui         | Contenu textuel du document.        |
| `metadata` | `object`   | Non         | Métadonnées associées au document.  |
| `id`       | `string`   | Oui         | Identifiant unique du document.     |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Confirmation de l'ajout du document.  

---

### 4. **Mettre à jour un document**  
- **Route** : `PUT /update_one_document`  
- **Tags** : Manage one document  
- **Paramètres d'entrée** :  

| Nom        | Type       | Obligatoire | Description                         |
|------------|------------|-------------|-------------------------------------|
| `document` | `string`   | Oui         | Nouveau contenu textuel du document.|
| `metadata` | `object`   | Non         | Nouvelles métadonnées associées.    |
| `id`       | `string`   | Oui         | Identifiant unique du document.     |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Confirmation de la mise à jour du document.  

---

### 5. **Supprimer un document**  
- **Route** : `PUT /delete_one_document`  
- **Tags** : Manage one document  
- **Paramètres d'entrée** :  

| Nom | Type     | Obligatoire | Description                         |
|-----|----------|-------------|-------------------------------------|
| `id`| `string` | Oui         | Identifiant unique du document.     |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Confirmation de la suppression du document.  

---

### 6. **Ajouter des documents**  
- **Route** : `POST /add_documents`  
- **Tags** : Manage documents  
- **Paramètres d'entrée** :  

| Nom         | Type            | Obligatoire | Description                                    |
|-------------|-----------------|-------------|------------------------------------------------|
| `documents` | `array[string]` | Oui         | Liste des contenus textuels des documents.    |
| `metadatas` | `array[object]` | Oui         | Liste des métadonnées associées.              |
| `ids`       | `array[string]` | Oui         | Liste des identifiants uniques des documents. |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Confirmation de l'ajout des documents.  

---

### 7. **Mettre à jour des documents**  
- **Route** : `PUT /update_documents`  
- **Tags** : Manage documents  
- **Paramètres d'entrée** :  

| Nom         | Type            | Obligatoire | Description                                    |
|-------------|-----------------|-------------|------------------------------------------------|
| `documents` | `array[string]` | Oui         | Liste des nouveaux contenus textuels.         |
| `metadatas` | `array[object]` | Oui         | Liste des nouvelles métadonnées associées.    |
| `ids`       | `array[string]` | Oui         | Liste des identifiants uniques des documents. |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Confirmation de la mise à jour des documents.  

---

### 8. **Supprimer des documents**  
- **Route** : `PUT /delete_documents`  
- **Tags** : Manage documents  
- **Paramètres d'entrée** :  

| Nom  | Type            | Obligatoire | Description                                    |
|------|-----------------|-------------|------------------------------------------------|
| `ids`| `array[string]` | Oui         | Liste des identifiants uniques des documents. |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Confirmation de la suppression des documents.  

---

### 9. **Compter les documents**  
- **Route** : `GET /count_documents`  
- **Tags** : Others  
- **Paramètres d'entrée** : Aucun  
- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Nombre total de documents présents dans la base.  

---

### 10. **Réinitialiser la collection**  
- **Route** : `POST /reset`  
- **Tags** : Others  
- **Paramètres d'entrée** : Aucun  
- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success` ou `failure`).  
  - `message` : Confirmation de la réinitialisation de la base.  
