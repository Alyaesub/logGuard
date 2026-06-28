import re
from log_parser import ( 
    read_log, 
    count_status, 
    count_fail_by_ip, 
    get_suspicious_ips,
    parse_log_lines,
  )
from reporter import (
  get_current_timestamp,
  show_summary,
  write_report,
  write_json_alerts,
)


#limite de tentative de co avant suspissions
THRESHOLD = 4

#récup le path mis en input
file_path = input("Entrez le nom du fichier a analyser : ")

#appel de la fonction qui lis le fichier mis en path
lines = read_log(file_path)
if not lines:
  print("Erreur, fichier inutilisable")
  exit(1)

#parsing des lignes centralisé et mis en liste
parsed_logs = parse_log_lines(lines) #liste qui sert de bd ou je stock les lines parsé

#appel de la fonction qui fait le compte des status de connexion
result = count_status(parsed_logs)

#variable qui stock le nombre de fail par ip
fail_by_ip = count_fail_by_ip(parsed_logs)

#variable qui stock les ip suspect
suspicious_ips = get_suspicious_ips(fail_by_ip, THRESHOLD)

#dict qui contient les parametre pour les function d'affichage et d'ecriture
report_data = {
  "file_path": file_path,
  "generated_at": get_current_timestamp(),
  "threshold": THRESHOLD,
  "parsed_count": len(parsed_logs),
  "success": result["success"],
  "fail": result["fail"],
  "fail_by_ip": fail_by_ip,
  "suspicious_ips": suspicious_ips,
}

#print le résumé
show_summary(report_data)

# appel la function qui ecrit le rapport
write_report(result, file_path, fail_by_ip, suspicious_ips, parsed_logs)
print("Rapport généré : reports/report.txt")

# appel la function qui ecrit le rapport d'alerte en JSON 
write_json_alerts(fail_by_ip, suspicious_ips)
print("Rapport généré : reports/alerts.json")


############# teste des fonctions ##########
