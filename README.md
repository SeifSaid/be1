# Qui utilise mon appli ? Identification des utilisateurs de Copilote

Projet MOD 7.2 (Introduction à la science des données), Centrale Lyon.
Challenge Kaggle : prédire quel utilisateur (parmi 247) a produit une session du logiciel Copilote, à partir du navigateur et de la suite d'actions.

## Contenu

| Fichier | Rôle |
|---|---|
| `analyse.ipynb` | notebook principal : exploration, modèles, résultats, soumission |
| `explore.ipynb` | première exploration des données |
| `submission.csv` | prédictions sur le test (format `RowId,prediction`) |
| `data/` | `train.csv`, `test.csv`, `sample_submission.csv` |

## Lancer

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ouvrir `analyse.ipynb` avec le noyau `.venv` et tout exécuter (environ 5 minutes).

## Démarche

1. **Lecture** ligne par ligne : les sessions vont de 0 à 12 000 actions, un tableau rectangulaire n'aurait pas de sens.
2. **Découpage des actions** : type d'action, écran `(…)`, configuration `<…>`, chaîne `$…$`, `1` final = modification. Les `tXX` sont des repères de temps.
3. **Exploration** : 3 279 sessions, 4 à 75 sessions par utilisateur, un seul navigateur par utilisateur, sessions longues gardées (réelles et présentes dans le test).
4. **Représentation** : chaque session devient un texte de « mots » (action, écran, configuration, chaîne, navigateur), vectorisé par TF-IDF avec bigrammes pour garder l'ordre des actions.
5. **Évaluation** : validation croisée stratifiée à 4 plis (l'utilisateur le plus rare a 4 sessions), TF-IDF dans le pipeline pour éviter toute fuite de données. Métrique : accuracy.

## Résultats

| Modèle | Accuracy (CV 4 plis) |
|---|---|
| Classe majoritaire | 2,3 % |
| Forêt aléatoire (variables résumées) | 85,1 % |
| Plus proche voisin (TF-IDF) | 89,4 % |
| Régression logistique (TF-IDF) | 93,3 % |
| SVM linéaire (TF-IDF, C = 0,5) | 94,7 % |
| **SVM linéaire réglé (C = 10)** | **96,2 %** |

Apport des informations (SVM, C = 0,5) : types d'action seuls 59,4 %, + bigrammes 84,7 %, + écrans, configurations et chaînes 94,1 %, + navigateur 94,7 %.

**À retenir :**
- l'ordre des actions et les écrans ou configurations utilisés identifient le mieux une personne ;
- les erreurs se concentrent sur les sessions courtes (90 %) et les utilisateurs ayant peu de sessions (93 %) ;
- le score de 96,2 % est légèrement optimiste, car C a été choisi sur les mêmes plis ; le score Kaggle sert de mesure indépendante.
