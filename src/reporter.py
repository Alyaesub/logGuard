from datetime import datetime
import json

#fonction qui récupére et fomate la date du jours pour mettre dans les rapport
def get_current_timestamp():
  now = datetime.now()
  formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")
  return formatted_date


#fonction qui résume et affiche le resultat dans le terminal
def show_summary(report_data):
  print("============= Résumé LogGuard =============")
  print(f"===== Nom du fichier : {report_data['file_path']} =====")
  print("Date du rapport:", report_data["generated_at"])
  print()
  print("Nombre de lignes exploitable:", report_data["parsed_count"])
  print()
  print("SUCCESS connexions:", report_data["success"])
  print("FAIL connexions:", report_data["fail"])
  print()
  print("IP suspectes:")
  if report_data["suspicious_ips"]:
    for ip in report_data["suspicious_ips"]:
      print(f" - {ip} : {report_data['fail_by_ip'][ip]} FAIL")
  else:
    print("Aucune IP suspecte détectée")
  print("===================================")

#function qui ouvre et ecrit un rapport.txt dans /reports
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

# function qui écrit un rapport d'alerte en JSON dans /reports
def write_json_alerts(fail_by_ip, suspicious_ips):
  alerts = []#créé un liste pour chaque ip
  
  if suspicious_ips:
    for ip in suspicious_ips:
      suspicious_ip_json = {
        "ip": ip,
        "fail_count": fail_by_ip[ip] 
      }
      alerts.append(suspicious_ip_json)
    
    with open("reports/alerts.json", "w") as f:
      json.dump(alerts, f, indent=2)