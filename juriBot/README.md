# Documentation de l'API JuriBot

## Fonctionnement de JuriBot

JuriBot est un agent virtuel utilisant le modèle de langage **Mistral**. Il est conçu pour répondre à des questions juridiques en utilisant des outils spécifiques, dont **`queryInformationsBySimilarity`**, qui recherche des documents juridiques pertinents en fonction de la requête utilisateur.

Le processus se déroule en plusieurs étapes :
1. **L'utilisateur pose une question** (avec ou sans historique de messages).
2. **L'agent analyse la question** :
   - Si une réponse directe est possible, elle est donnée.
   - Si une recherche est nécessaire, l'outil **`queryInformationsBySimilarity`** est automatiquement utilisé pour trouver des articles de code pertinents.
3. **Mise à jour du contexte** : Les résultats de la recherche sont ajoutés au contexte de la conversation.
4. **L'agent génère une réponse finale** en tenant compte du contexte enrichi.
5. **L'ensemble des messages échangés** (y compris ceux générés par l'outil) est renvoyé à l'utilisateur.

## Endpoints de l'API

### 1. **Vérification de la santé**  
- **Route** : `GET /health_check`  
- **Tags** : Monitoring  
- **Description** : Vérifie si l'application est en cours d'exécution et fonctionnelle.  

- **Champs de sortie** :  
  - `status` : Le statut de l'exécution (`success`).  
  - `message` : Message de confirmation que la vérification est réussie.

---

### 2. **Requête par similarité**  
- **Route** : `GET /query`  
- **Tags** : Querying  
- **Description** : Recherche des documents juridiques pertinents en fonction de la requête utilisateur, en utilisant l'outil **`queryInformationsBySimilarity`**.

- **Paramètres d'entrée** :

| Nom        | Type          | Obligatoire | Description                                       |
|------------|---------------|-------------|---------------------------------------------------|
| `query`    | `string`      | Oui         | Texte de la requête.                             |
| `n_results`| `integer`     | Non         | Nombre maximal de résultats à retourner. Par défaut, 5. |
| `include`  | `array[string]` | Non         | Informations à inclure dans la réponse (`ids`, `documents`, `metadatas`, `distances`). Par défaut, `['documents', 'metadatas']`. |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success`).  
  - `results` : Liste des documents pertinents trouvés par l'outil de similarité. Chaque résultat inclut les informations demandées (comme `documents`, `metadatas`, etc.).

---

### 3. **Appel de l'Agent**  
- **Route** : `GET /chat`  
- **Tags** : RAG  
- **Description** : Permet à l'utilisateur d'interagir avec l'agent **JuriBot**, qui répond en fonction de la question et de l'historique des messages.

- **Paramètres d'entrée** :

| Nom             | Type              | Obligatoire | Description                                           |
|-----------------|-------------------|-------------|-------------------------------------------------------|
| `user_query`    | `string`          | Oui         | Question de l'utilisateur.                            |
| `history_messages` | `array[dict]`  | Non         | Historique des messages précédents, peut être vide.  |

- **Champs de sortie** :  
  - `status` : Statut de l'exécution (`success`).  
  - `messages` : Liste des messages échangés, y compris la réponse finale générée par l'agent.

---

### 4. **Gestion de l'historique et des documents**  
L'agent utilise **l'outil `queryInformationsBySimilarity`** en **`tool_choice="any"`**, ce qui implique que cet outil est toujours utilisé lorsqu'une recherche de documents est nécessaire. Cela permet à l'agent de toujours inclure les documents pertinents dans le contexte de la réponse.

#### Exemple de fonctionnement :
Lorsqu'un utilisateur pose une question liée à un aspect spécifique du droit, l'agent utilise l'outil **`queryInformationsBySimilarity`** pour récupérer les documents les plus pertinents et les ajouter au contexte de la conversation. Ce processus garantit que la réponse fournie est toujours basée sur les documents les plus récents et pertinents disponibles.

---

## Structure de l'Agent JuriBot

- **Mistral Client** : Utilisé pour envoyer des requêtes au modèle de langage **Mistral** et recevoir des réponses.
- **Système de prompt** : Un fichier `system_prompt.txt` contient le prompt de base utilisé pour initialiser le modèle.
- **Outils disponibles** : L'outil **`queryInformationsBySimilarity`** est utilisé pour effectuer des recherches de documents législatifs pertinents.
- **Gestion des outils** : Le paramètre `tool_choice` est défini sur `"any"`, ce qui implique que l'outil est toujours utilisé lors de chaque interaction.

---

## Exemple d'Utilisation

1. L'utilisateur pose une question sur un aspect du droit de l'éducation.
2. L'agent utilise l'outil **`queryInformationsBySimilarity`** pour rechercher les articles de loi pertinents.
3. L'agent met à jour l'historique des messages en ajoutant les résultats de la recherche.
4. Une réponse finale est générée en tenant compte des documents juridiques trouvés.
5. L'ensemble des messages (question initiale, réponse générée, résultats des outils) est renvoyé à l'utilisateur.

---

### Notes :

- **Outils** : L'outil **`queryInformationsBySimilarity`** est toujours utilisé (car `tool_choice = "any"`) chaque fois qu'une recherche est nécessaire pour fournir une réponse complète et pertinente.
- **Réponse** : Les résultats des recherches sont renvoyés dans le contexte de la conversation, ce qui permet une interaction dynamique et en constante évolution avec l'agent.
