# LogGuard

## Description

LogGuard est un outil CLI développé en Python dans le cadre d'un apprentissage orienté cybersécurité et DevSecOps.

Son objectif est d'analyser des fichiers de logs afin d'extraire des informations utiles, détecter des comportements suspects et générer des rapports d'analyse.

Le projet est construit progressivement en suivant une roadmap Python tout en conservant une architecture évolutive afin de pouvoir analyser différents formats de logs à terme.

---

# Fonctionnalités actuelles

## Lecture des logs

- Lecture d'un fichier texte (`.txt`, `.log`)
- Gestion des erreurs d'ouverture de fichier
- Suppression des lignes vides
- Nettoyage des lignes avec `strip()`

## Parsing des logs

Chaque ligne est transformée en objet Python contenant les informations exploitables.

Informations actuellement extraites :

- Timestamp
- Statut de connexion (`SUCCESS` / `FAIL`)
- Utilisateur
- Adresse IP

Les lignes invalides sont ignorées.

---

## Analyse

- Comptage des connexions SUCCESS
- Comptage des connexions FAIL
- Comptage des FAIL par adresse IP
- Détection des adresses IP suspectes selon un seuil configurable

---

## Résumé

Affichage dans le terminal :

- Nom du fichier analysé
- Nombre de lignes exploitables
- Nombre de SUCCESS
- Nombre de FAIL
- Liste des IP suspectes
- Nombre de FAIL par IP suspecte

---

# Structure actuelle

```text
logGuard/
│
├── ressources/
│   └── logs_simple.txt
│
├── src/
│   ├── main.py
│   ├── log_parser.py
│   ├── reporter.py
│   └── network_tools.py
│
└── README.md
```

---

# Lancement

Depuis la racine du projet :

```bash
python3 src/main.py
```

Puis saisir le chemin du fichier :

```text
ressources/logs_simple.txt
```

---

# Configuration

Le seuil de détection est défini dans `main.py` :

```python
THRESHOLD = 4
```

Une adresse IP est considérée comme suspecte lorsque son nombre d'échecs de connexion atteint ou dépasse cette valeur.

---

# Architecture actuelle

Le projet est organisé autour de plusieurs responsabilités.

## `log_parser.py`

Lecture et parsing des logs.

Fonctions :

- `read_log()`
- `extract_status()`
- `extract_ip()`
- `extract_user()`
- `extract_timestamp()`
- `parse_log_line()`
- `count_status()`
- `count_fail_by_ip()`
- `is_suspicious()`
- `get_suspicious_ips()`

---

## `reporter.py`

Affichage des résultats.

Fonctions :

- `show_summary()`

---

## `main.py`

Point d'entrée de l'application.

Responsabilités :

- lecture du fichier
- parsing des logs
- lancement des analyses
- affichage du résumé

---

# Évolutions prévues

- Génération d'un rapport texte (`report.txt`)
- Export JSON (`alerts.json`)
- Utilisation de `argparse`
- Ajout du module `logging`
- Horodatage avec `datetime`
- Support de plusieurs formats de logs (SSH, Apache, Nginx…)
- Scanner réseau des IP suspectes
- Génération de rapports plus complets

---

# Objectif du projet

Au-delà de l'apprentissage de Python, LogGuard a pour objectif de devenir un véritable outil d'analyse de logs orienté cybersécurité, construit progressivement avec une architecture propre, modulaire et facilement extensible.
