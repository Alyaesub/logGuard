from log_parser import ( 
    read_log, 
    count_status, 
    count_fail_by_ip, 
    get_suspicious_ips 
  )

#limite de tentative de co avant suspissions
THRESHOLD = 4

#récup le path mis en input
file_path = input("Entrez le nom du fichier a analyser : ")

#appel de la fonction qui lis le fichier mis en path
lines = read_log(file_path)

#appel de la fonction qui fait le compte des status de connexion
result = count_status(lines)

#fonction qui résume et affiche le resultat de read_log et count_status
def show_summary(result, file_path,  fail_by_ip, suspicious_ips):
  print("===== Résumé LogGuard =====")
  print(f"===== Nom du fichier : {file_path} =====")
  print("SUCCESS :", result["success"])
  print("FAIL :", result["fail"])
  print("FAIL by IP :", fail_by_ip)
  print("IP suspect :", suspicious_ips)
  print("===================================")

#variable qui stock le nombre de fail par ip
fail_by_ip = count_fail_by_ip(lines)

#variable qui stock les ip suspect
suspicious_ips = get_suspicious_ips(fail_by_ip, THRESHOLD)

#print le résumé
show_summary(result, file_path)