from datetime import datetime

#fonction qui récupére et fomate la date du jours pour mettre dans les rapport
def get_current_timestamp():
  now = datetime.now()
  formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")
  return formatted_date


#fonction qui résume et affiche le resultat de read_log et count_status
def show_summary(result, file_path,  fail_by_ip, suspicious_ips, parsed_logs):
  print("============= Résumé LogGuard =============")
  print(f"===== Nom du fichier : {file_path} =====")
  print()
  print("Nombre de lignes exploitable:", len(parsed_logs))
  print()
  print("SUCCESS connexions:", result["success"])
  print("FAIL connexions:", result["fail"])
  print()
  print("IP suspectes:")
  if suspicious_ips:
    for ip in suspicious_ips:
      print(f" - {ip} : {fail_by_ip[ip]} FAIL")
  else:
    print("Aucune IP suspecte détectée")
  print("===================================")

#function qui ouvre et ecrit un rapport dans /reports
def write_report(result, file_path, fail_by_ip, suspicious_ips, parsed_logs):
  with open('reports/report.txt', 'w') as f:
    f.write("====== LogGuard Report ======\n")
    f.write(f"Date du rapport: {get_current_timestamp()}\n")
    f.write(f"Nom du fichier: {file_path}\n")
    f.write(f"Nombre de lignes exploitable: {len(parsed_logs)}\n")
    f.write("\n")
    f.write(f"SUCCESS connexions: {result['success']}\n")
    f.write(f"FAIL connexions: {result['fail']}\n")
    f.write("\n")
    f.write(f"FAIL by IP:\n")
    for ip, count in fail_by_ip.items():
      f.write(f" - {ip} : {count} FAIL\n")
    f.write("\n")
    f.write(f"IP suspectes:\n")
    if suspicious_ips:
      for ip in suspicious_ips:
        f.write(f" - {ip} : {fail_by_ip[ip]} FAIL\n")
    else:
      f.write("Aucune IP suspecte détectée\n")