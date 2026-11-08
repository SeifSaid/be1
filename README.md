# Qui utilise mon appli ? Identification des utilisateurs de Copilote

Projet du MOD 7.2 (Introduction à la science des données), Centrale Lyon, groupe TD 4.
Seifeddine Said, Souhaib Zabi, Abdelhak Tantaoui.

Challenge Kaggle : retrouver l'utilisateur (parmi 247) qui a produit une session du logiciel Copilote, à partir du navigateur et de la suite des actions.

## Contenu

| Fichier | Rôle |
|---|---|
| `analyse.ipynb` | notebook principal : exploration, représentation, modèles, analyse des erreurs, soumission |
| `rapport/` | rapport LaTeX (classe `rapportECL`) et figures |
| `submission_v1_svm.csv` | prédictions sur le test, SVM seul |
| `submission_v2_svm_navigateur.csv` | prédictions sur le test, SVM + contrainte du navigateur (version finale) |
| `consignes/` | consignes et indications du BE |
| `requirements.txt` | dépendances (Python 3.14) |

## Données

Les données ne sont pas incluses. Télécharger `train.csv`, `test.csv` et `sample_submission.csv` depuis la [page du challenge](https://www.kaggle.com/competitions/qui-utilise-mon-appli-challenge/data) et les placer dans `data/`.

Chaque ligne contient l'utilisateur (train uniquement), le navigateur, puis les actions de la session. Une action peut indiquer un écran `(...)`, une configuration d'écran `<...>`, une chaîne `$...$` et un `1` final si la fiche est en modification. Les jetons `tXX` sont des repères de temps en secondes.

## Exécution

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ouvrir `analyse.ipynb` avec le noyau `.venv` et tout exécuter (environ 8 minutes). Le notebook écrit les deux fichiers de soumission et les figures du rapport.

## Démarche

1. Lecture de chaque session comme une liste d'actions (de 0 à 12 000 actions par session).
2. Découpage de chaque action en type, écran, configuration, chaîne et mode modification.
3. Exploration : 3 279 sessions, 4 à 75 sessions par utilisateur, un seul navigateur par utilisateur, sessions longues conservées.
4. Représentation : chaque session devient un texte de mots, vectorisé par TF-IDF avec bigrammes (9 002 mots).
5. Évaluation : validation croisée stratifiée à 4 plis, TF-IDF dans le pipeline ; accuracy et F1 macro.
6. Modèle : SVM linéaire, C = 10, choisi par validation croisée répétée.
7. Post-traitement : seuls les utilisateurs du navigateur de la session sont retenus.

## Résultats

| Modèle | Accuracy (CV) | F1 macro (CV) | Kaggle |
|---|---|---|---|
| Classe majoritaire | 2,3 % | 0,0 % | |
| Forêt aléatoire (43 variables) | 85,1 % | 81,9 % | |
| Plus proche voisin (TF-IDF) | 89,4 % | 87,6 % | |
| Régression logistique réglée (TF-IDF, C = 100) | 94,7 % | 93,2 % | |
| SVM linéaire réglé (TF-IDF, C = 10) | 96,2 % | 95,8 % | 0,963 |
| SVM + contrainte du navigateur | 97,2 % | 96,9 % | 0,982 |

- L'enchaînement des actions (bigrammes) et les écrans utilisés apportent chacun autant, et sont complémentaires.
- 61 des 125 erreurs du SVM désignaient un utilisateur d'un autre navigateur ; la contrainte corrige ces erreurs.
- Trigrammes, rééquilibrage des classes et repères de temps n'apportent pas de gain mesurable.
- Les erreurs restantes concernent surtout les sessions courtes et quelques paires d'utilisateurs qui travaillent sur les mêmes écrans.
