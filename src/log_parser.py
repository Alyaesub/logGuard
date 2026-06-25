#fonction qui lis le fichier mis en path
def read_log(path):
  try:
    with open(path) as file:
        lines = file.readlines()
  except FileNotFoundError:
    print("Erreur: Fichier introuvable")
    return []
  
  clean_lines = []
      
  for line in lines:
    clean_line = line.strip()
    if clean_line != "":
      clean_lines.append(clean_line)
  
  return clean_lines

#fonction qui analyse le statut d'une ligne
# pour plus tard rajouter des status en fonction des formats
def extract_status(line):
  if "SUCCESS" in line:
    return "SUCCESS"
  elif "FAIL" in line:
    return "FAIL"
  return None

#fonction qui fait le compte des status de connexion
def count_status(parsed_logs):
  success = 0
  fail = 0
  
  for log in parsed_logs:
      if log["status"] == "SUCCESS":
        success += 1
      if log["status"] == "FAIL":
        fail += 1
      
  return {
    "success": success,
    "fail": fail
  }

#function qui récupére l'ip
def extract_ip(line):
  parts = line.split()
  
  for part in parts:
    if part.startswith("ip="):
      ip = part.split("=")[1]
      
      return ip
  
  return None

#function qui recupére le user
def extract_user(line):
  parts = line.split()
  
  for part in parts:
    if part.startswith("user="):
      user = part.split("=") [1]
      return user
  
  return None

#function qui récupe le timestamp
def extract_timestamp(line):
  parts = line.split()
  
  if len(parts) >= 2:
    date = parts[0]
    heure = parts[1]
    
    return f"{date} {heure}"
  
  return None

#function qui compte les tentative fail de co d'une ip
def is_suspicious(count, threshold):
  if count >= threshold:
    return True
  else:
    return False

#function qui compte le nombre fail par IP
def count_fail_by_ip(parsed_logs):
  fail_by_ip = {}
  
  for log in parsed_logs:
      if log["status"] == "FAIL":
        if log["ip"] not in fail_by_ip:
          fail_by_ip[log["ip"]] = 1
        else:
          fail_by_ip[log["ip"]] += 1
  
  return fail_by_ip

#function qui stock les IP suspectes
def get_suspicious_ips(fail_by_ip, threshold):
  suspicious_ips = []
  
  for ip, count in fail_by_ip.items():
    if is_suspicious(count, threshold):
      suspicious_ips.append(ip)
        
  return suspicious_ips

# function qui parse une ligne de logue
# pour plus tard rajouter des status en fonction des formats
def parse_log_line(line):
  status = extract_status(line)
  ip = extract_ip(line)
  user = extract_user(line)
  timestamp = extract_timestamp(line)
  
  if status is None:
    return None
  if ip is None:
    return None
  
  return {
    "status": status,
    "ip": ip,
    "user": user,
    "timestamp": timestamp
  }