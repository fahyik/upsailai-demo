```
├── Dockerfile  
├── Makefile  
├── app   
│   ├── README.md  
│   ├── __init__.py  
│   ├── chat  
│   │   ├── __init__.py  
│   │   ├── chain.py  
│   │   └── routes.py  
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── main.py                     # FastAPI Application
│   ├── routes.py
│   └── utils
│       ├── __init__.py
│       └── logging.py
├── bot
│   ├── __init__.py
│   ├── bot.py
│   ├── command.py
│   ├── config.py
│   ├── handlers
│   │   ├── __init__.py
│   │   ├── base_handler.py
│   │   ├── image_handler.py
│   │   └── text_handler.py
│   ├── healthcheck.py
│   ├── main.py
│   └── views.py
├── chains
│   ├── __init__.py
│   ├── chain_manager.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── suggestions.py
│   ├── modules
│   │   ├── __init__.py
│   │   ├── embeddings.py           # CLIPembeddings for text and image (get_image_features)
│   │   ├── splitter.py             # diviser un document produit en plusieurs sous-documents basés sur ses attributs (images, couleur, style, occasions, saisons, météo, description).
│   │   └── vectorstore.py          # class MulitModalChroma
│   ├── retriever.py                # load_retriever
│   ├── sale_assistant_chain.py
│   ├── stylist_chain.py
│   └── utils
│       ├── __init__.py
│       ├── formatter.py
│       └── util.py
├── requirements.txt
└── wsgi.py
```

**main.py**
**Keyword**: FastAPI Application

**Description**: Ce fichier configure et lance une application FastAPI avec des routes pour le chat, une configuration de middleware CORS, et un point de terminaison de vérification de l'état (/ready).

**routes.py**
**Keyword**: Chat API Routes

**Description**: Ce fichier définit les routes API pour le chat, y compris les points de terminaison pour envoyer des messages et obtenir des recommandations de produits, en utilisant FastAPI.

**retriever.py**: # Ce fichier définit une fonction load_retriever qui configure et retourne un ParentDocumentRetriever utilisant un MultiModalChroma pour la vectorisation des documents, un ProductDocumentSplitter pour la division des documents, et un LocalFileStore pour le stockage local des documents.

splitter.py
Keyword: ProductDocumentSplitter

Description: Ce fichier définit la classe ProductDocumentSplitter qui hérite de TextSplitter et implémente la méthode _split_document pour diviser un document produit en plusieurs sous-documents basés sur ses attributs (images, couleur, style, occasions, saisons, météo, description).

embeddings.py
Keyword: CLIPEmbeddings

Description: Ce fichier définit la classe CLIPEmbeddings qui utilise le modèle CLIP pour générer des embeddings de texte et d'images encodées en base64, permettant ainsi la vectorisation de documents multimodaux.