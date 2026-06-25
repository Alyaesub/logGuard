from log_parser import ( 
    read_log, 
    count_status, 
    count_fail_by_ip, 
    get_suspicious_ips,
    parse_log_line,
  )
from reporter import (
  show_summary,
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
parsed_logs = [] #liste qui sert de bd ou je stock les lines parsé

for line in lines:
  parsed = parse_log_line(line)
  if parsed is not None:
    parsed_logs.append(parsed)

#appel de la fonction qui fait le compte des status de connexion
result = count_status(parsed_logs)

#variable qui stock le nombre de fail par ip
fail_by_ip = count_fail_by_ip(parsed_logs)

#variable qui stock les ip suspect
suspicious_ips = get_suspicious_ips(fail_by_ip, THRESHOLD)

#print le résumé
show_summary(result, file_path, fail_by_ip, suspicious_ips, parsed_logs)