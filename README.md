# LogGuard

## Description

LogGuard est un mini outil CLI développé en Python dans le cadre d'un apprentissage orienté cybersécurité.

Son objectif est d'analyser des fichiers de logs de connexion afin de détecter des comportements suspects comme des tentatives répétées d'authentification.

---

## Fonctionnalités actuelles

### Lecture des logs

- Lecture d'un fichier texte
- Nettoyage des lignes avec `strip()`

### Analyse des connexions

- Comptage des connexions SUCCESS
- Comptage des connexions FAIL

### Analyse des adresses IP

- Extraction des IP depuis les logs
- Comptage du nombre de FAIL par IP
- Détection des IP suspectes selon un seuil configurable

### Résumé

Affichage :

- Nom du fichier analysé
- Nombre total de SUCCESS
- Nombre total de FAIL
- Nombre de FAIL par IP
- Liste des IP suspectes

---

## Structure du projet

```text
logGuard/
│
├── main.py
├── log_parser.py
├── network_tools.py
├── logs.txt
└── README.md
```

---

## Lancement

```bash
python3 main.py
```

Puis saisir le fichier à analyser :

```text
logs.txt
```

---

## Seuil de détection

Dans `main.py` :

```python
THRESHOLD = 4
```

Une IP est considérée comme suspecte lorsqu'elle atteint ou dépasse ce nombre d'échecs de connexion.

---

## Fonctions actuelles

### log_parser.py

- `read_log(path)`
- `count_status(lines)`
- `extract_ip(line)`
- `is_suspicious(count, threshold)`
- `count_fail_by_ip(lines)`
- `get_suspicious_ips(fail_by_ip, threshold)`

### main.py

- `show_summary(...)`

---
