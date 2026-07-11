import argparse
import logging

from log_parser import ( 
    read_log, 
    count_status, 
    count_fail_by_ip, 
    get_suspicious_ips,
    parse_log_lines,
    count_fail_by_user,
  )
from reporter import (
  get_current_timestamp,
  show_summary,
  write_report,
  write_json_alerts,
)
from network_tools import (
  scan_suspicious_ips,
  reverse_dns_suspicious_ips,
  check_http_suspicious_ips,
)

############ config de la lib Logging
logging.basicConfig(
    level=logging.INFO, #affiche les messages INFO, WARNING, ERROR
    format="%(levelname)s - %(message)s"
)
#####################################

################### argparse et commande CLI
parser = argparse.ArgumentParser(description="Parser de fichier de logs")
parser.add_argument("--file", required=True, help="argument obligatoire : fichier logs")
parser.add_argument(
    "--threshold",
    type=int,
    default=4,
    help="Seuil de FAIL à partir duquel une IP est suspecte"
)
args = parser.parse_args()
############################################

#limite de tentative de co avant suspissions
THRESHOLD = args.threshold

#récup le path mis en input
file_path = args.file
logging.info("Début de l'analyse")
logging.info(f"Fichier reçu : {file_path}")

#appel de la fonction qui lis le fichier mis en path
lines = read_log(file_path)
if not lines:
  print("Erreur, fichier inutilisable")
  exit(1)

#parsing des lignes centralisé et mis en liste
parsed_logs = parse_log_lines(lines) #liste qui sert de bd ou je stock les lines parsé
logging.info(f"{len(parsed_logs)} lignes exploitables")

#appel de la fonction qui fait le compte des status de connexion
result = count_status(parsed_logs)

#variable qui stock le nombre de fail par ip
fail_by_ip = count_fail_by_ip(parsed_logs)

#variable qui stock les ip suspect
suspicious_ips = get_suspicious_ips(fail_by_ip, THRESHOLD)
logging.warning(f"{len(suspicious_ips)} IP suspectes détectées")

#variable qui stock les fails par user
fail_by_user = count_fail_by_user(parsed_logs)

#variable qui stock les scan des IP suspecte
scanned_suspicious_ips = scan_suspicious_ips(suspicious_ips, [443, 22, 80])

#variable qui stock les revers DNS des ips suspectes
reverse_dns_by_ip = reverse_dns_suspicious_ips(suspicious_ips)
logging.warning(f"{len(reverse_dns_by_ip)} DNS détectées")

#variable qui stock les requetes HTTP sur les ports des IP suspectes
http_checks_by_ip = check_http_suspicious_ips(scanned_suspicious_ips)

#dict qui contient les parametre pour les function d'affichage et d'ecriture
report_data = {
  "file_path": file_path,
  "generated_at": get_current_timestamp(),
  "threshold": THRESHOLD,
  "parsed_count": len(parsed_logs),
  "success": result["success"],
  "fail": result["fail"],
  "fail_by_ip": fail_by_ip,
  "fail_by_user": fail_by_user,
  "suspicious_ips": suspicious_ips,
  "scanned_suspicious_ips": scanned_suspicious_ips,
  "reverse_dns_by_ip": reverse_dns_by_ip,
  "http_checks_by_ip": http_checks_by_ip,
}

#print le résumé
show_summary(report_data)

# appel la function qui ecrit le rapport
write_report(report_data)
logging.info("Rapport texte généré")

# appel la function qui ecrit le rapport d'alerte en JSON 
write_json_alerts(report_data)
logging.info("Rapport JSON généré")


############# teste des fonctions ##########
