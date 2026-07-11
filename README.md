# LogGuard

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Version](https://img.shields.io/badge/version-1.0-success)
![License](https://img.shields.io/badge/license-MIT-green)

LogGuard est un outil CLI Python d’analyse de logs orienté cybersécurité.

Il extrait les événements de connexion, détecte les tentatives répétées d’authentification, identifie les adresses IP suspectes et enrichit les résultats avec des informations réseau.

Le programme produit un résumé dans le terminal ainsi que des rapports aux formats texte et JSON.

---

## Fonctionnalités

- Lecture de fichiers `.txt` et `.log`
- Gestion des fichiers introuvables et des lignes invalides
- Nettoyage et parsing des lignes
- Support de plusieurs formats de logs :
    - format simple `key=value`
    - logs SSH de type `auth.log`

- Extraction :
    - timestamp
    - statut `SUCCESS` ou `FAIL`
    - utilisateur
    - adresse IP

- Comptage des connexions réussies et échouées
- Comptage des échecs par adresse IP
- Comptage des échecs par utilisateur
- Détection des IP suspectes selon un seuil configurable
- Scan TCP des IP suspectes
- Vérification des ports `22`, `80` et `443`
- Résolution DNS inverse
- Vérification HTTP et HTTPS des ports web ouverts
- Journalisation technique avec `logging`
- Génération de rapports :
    - `reports/report.txt`
    - `reports/alerts.json`

- Interface en ligne de commande avec `argparse`

---

## Structure du projet

```text
logGuard/
├── reports/
│   ├── alerts.json
│   └── report.txt
├── ressources/
│   ├── logs_simple.txt
│   ├── logs_mixed.txt
│   └── logs_ssh.log
├── src/
│   ├── log_parser.py
│   ├── main.py
│   ├── network_tools.py
│   └── reporter.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

### Modules

- `main.py` : point d’entrée et orchestration du programme
- `log_parser.py` : lecture, parsing et analyse des logs
- `network_tools.py` : scan TCP, reverse DNS et vérification HTTP
- `reporter.py` : affichage terminal et génération des rapports

---

## Installation

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd logGuard
```

### 2. Créer un environnement virtuel

```bash
python3.12 -m venv .venv
```

### 3. Activer l’environnement

Sur macOS ou Linux :

```bash
source .venv/bin/activate
```

Sur Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

---

## Utilisation

Depuis la racine du projet :

```bash
python src/main.py --file ressources/logs_simple.txt
```

Avec un seuil personnalisé :

```bash
python src/main.py \
  --file ressources/logs_ssh.log \
  --threshold 3
```

### Arguments CLI

| Argument       | Obligatoire | Description                                                                     |
| -------------- | ----------: | ------------------------------------------------------------------------------- |
| `--file`       |         Oui | Chemin du fichier de logs à analyser                                            |
| `--threshold`  |         Non | Nombre de FAIL à partir duquel une IP devient suspecte. Valeur par défaut : `4` |
| `-h`, `--help` |         Non | Affiche l’aide générée par `argparse`                                           |

Afficher l’aide :

```bash
python src/main.py --help
```

---

## Exemple de sortie

```text
============= Résumé LogGuard =============

Nom du fichier : ressources/logs_ssh.log
Date du rapport : 29-06-2026 19:40:27

Nombre de lignes exploitables : 23

SUCCESS connexions : 6
FAIL connexions : 17

FAIL by User:
 - root : 8 FAIL
 - admin : 5 FAIL

IP suspectes:
 - 192.168.1.45 : 4 FAIL
 - 203.0.113.9 : 6 FAIL

Scan des ports des IP suspectes:
 - 192.168.1.45:
    22 : CLOSED
    80 : CLOSED
    443 : CLOSED

Reverse DNS des IP suspectes:
 - 192.168.1.45 : None

Statut HTTP des ports ouverts:
 - 192.168.1.45:
    Aucun port web ouvert
```

---

## Rapports générés

### Rapport texte

```text
reports/report.txt
```

Il contient :

- le fichier analysé
- la date de génération
- le nombre de lignes exploitables
- les totaux `SUCCESS` et `FAIL`
- les échecs par IP
- les échecs par utilisateur
- les IP suspectes
- les résultats du scan TCP
- les résultats du reverse DNS
- les résultats HTTP

### Rapport JSON

```text
reports/alerts.json
```

Exemple simplifié :

```json
{
	"file_path": "ressources/logs_ssh.log",
	"generated_at": "29-06-2026 19:40:27",
	"threshold": 4,
	"parsed_count": 23,
	"success": 6,
	"fail": 17,
	"fail_by_user": {
		"root": 8,
		"admin": 5
	},
	"alerts": [
		{
			"ip": "192.168.1.45",
			"fail_count": 4
		}
	],
	"scanned_suspicious_ips": {
		"192.168.1.45": {
			"22": false,
			"80": false,
			"443": false
		}
	},
	"reverse_dns_by_ip": {
		"192.168.1.45": null
	},
	"http_checks_by_ip": {
		"192.168.1.45": {}
	}
}
```

---

## Formats de logs supportés

### Format simple

```text
2026-05-13 10:01:22 LOGIN SUCCESS user=admin ip=192.168.1.10
2026-05-13 10:02:11 LOGIN FAIL user=root ip=192.168.1.45
```

### Format SSH

```text
Jun 25 14:31:15 ubuntu sshd[1234]: Failed password for root from 192.168.1.45 port 49822 ssh2
Jun 25 14:31:25 ubuntu sshd[1234]: Accepted password for admin from 192.168.1.10 port 49830 ssh2
```

Les lignes ne contenant pas suffisamment d’informations sont ignorées sans interrompre l’analyse.

---

## Limites de la version 1.0

- Les extracteurs couvrent principalement le format simple et certains logs SSH.
- Le scan TCP ne remplace pas un outil spécialisé comme Nmap.
- Un port TCP ouvert ne garantit pas qu’un service applicatif fonctionne correctement.
- Le reverse DNS peut retourner `None`.
- Les vérifications HTTP concernent actuellement les ports `80` et `443`.
- Les résultats réseau peuvent varier selon le timeout, le pare-feu, le VPN ou la configuration de la cible.
- Les scans doivent uniquement être réalisés sur des systèmes autorisés.

---

## Roadmap

### Version 1.1

- [ ] Ajouter `investigate_ip(ip)`
- [ ] Regrouper scan TCP, reverse DNS et HTTP
- [ ] Ajouter des ports personnalisables avec `--ports`
- [ ] Ajouter une option `--scan`
- [ ] Améliorer la gestion des erreurs réseau
- [ ] Ajouter des tests unitaires
- [ ] Refactoriser `network_tools.py`

### Version 1.2

- [ ] Export CSV
- [ ] GeoIP
- [ ] WHOIS
- [ ] Reverse DNS avancé
- [ ] Scan UDP
- [ ] Support Apache et Nginx

### Version 2.0

- [ ] Système de plugins
- [ ] Support avancé des logs SSH
- [ ] Support des événements Windows
- [ ] Image Docker
- [ ] API REST
- [ ] Interface web
- [ ] Intégration Wazuh ou Elastic

---

## Sécurité et usage responsable

LogGuard est un projet pédagogique.

Les fonctionnalités réseau doivent uniquement être utilisées sur :

- vos propres machines
- votre réseau local
- vos machines virtuelles
- vos conteneurs
- des systèmes pour lesquels vous disposez d’une autorisation explicite

L’utilisateur est responsable de son utilisation.

---

## Contributions

Les retours, propositions et contributions sont les bienvenus.

Les améliorations peuvent être proposées avec :

- une issue GitHub
- une pull request
- une description claire du problème ou de la fonctionnalité

---

## Licence

Ce projet est distribué sous licence MIT.

Consultez le fichier `LICENSE` pour plus d’informations.
