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