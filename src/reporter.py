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
  print()
  print(f"===== Nom du fichier : {report_data['file_path']} =====")
  print()
  print("Date du rapport:", report_data["generated_at"])
  print()
  print("Nombre de lignes exploitable:", report_data["parsed_count"])
  print()
  print("SUCCESS connexions:", report_data["success"])
  print("FAIL connexions:", report_data["fail"])
  print()
  print("FAIL by user:")
  if report_data["fail_by_user"]:
    for user in report_data["fail_by_user"]:
      print(f" - {user} : {report_data['fail_by_user'][user]} FAIL")
  else:
    print("Aucun User suspect détectée")
  print()
  print("IP suspectes:")
  if report_data["suspicious_ips"]:
    for ip in report_data["suspicious_ips"]:
      print(f" - {ip} : {report_data['fail_by_ip'][ip]} FAIL")
  else:
    print("Aucune IP suspecte détectée")
  print("===================================")

#function qui ouvre et ecrit un rapport.txt dans /reports
def write_report(report_data):
  with open('reports/report.txt', 'w') as f:
    f.write("====== LogGuard Report ======\n")
    f.write("\n")
    f.write(f"Date du rapport: {report_data['generated_at']}\n")
    f.write(f"Nom du fichier: {report_data['file_path']}\n")
    f.write(f"Nombre de lignes exploitable: {report_data['parsed_count']}\n")
    f.write("\n")
    f.write(f"SUCCESS connexions: {report_data['success']}\n")
    f.write(f"FAIL connexions: {report_data['fail']}\n")
    f.write("\n")
    f.write(f"FAIL by IP:\n")
    for ip, count in report_data["fail_by_ip"].items():
      f.write(f" - {ip} : {count} FAIL\n")
    f.write("\n")
    f.write(f"FAIL by User:\n")
    for user, count in report_data["fail_by_user"].items():
      f.write(f" - {user} : {count} FAIL\n")
    f.write("\n")
    f.write(f"IP suspectes:\n")
    if report_data["suspicious_ips"]:
      for ip in report_data["suspicious_ips"]:
        f.write(f" - {ip} : {report_data['fail_by_ip'][ip]} FAIL\n")
    else:
      f.write("Aucune IP suspecte détectée\n")

# function qui écrit un rapport d'alerte en JSON dans /reports
def write_json_alerts(report_data):
  alerts = []# liste des alerts ip
  
  if report_data["suspicious_ips"]:
    for ip in report_data["suspicious_ips"]:
      suspicious_ip_json = {
        "ip": ip,
        "fail_count": report_data["fail_by_ip"][ip]
      }
      alerts.append(suspicious_ip_json)
    
  json_report = {
    "file_path":report_data["file_path"],
    "generated_at": report_data["generated_at"],
    "threshold": report_data["threshold"],
    "parsed_count": report_data["parsed_count"],
    "success": report_data["success"],
    "fail": report_data["fail"],
    "fail_by_user": report_data["fail_by_user"],
    "alerts": alerts,
  }
  
  with open("reports/alerts.json", "w") as f:
    json.dump(json_report, f, indent=2)