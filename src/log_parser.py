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
  #format .txt
  if "SUCCESS" in line:
    return "SUCCESS"
  elif "FAIL" in line:
    return "FAIL"
  
  #format ssh.log
  if "Accepted password" in line:
    return "SUCCESS"
  if "Failed password" in line:
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
  
  for i in range(len(parts)):
    # Format txt
    if parts[i].startswith("ip="):
      ip = parts[i].split("=")[1]
      return ip
      # format ssh.log
    elif parts[i].startswith("from"):
      if i + 1 < len(parts):
        return parts[i + 1]
  
  return None

#function qui recupére le user
def extract_user(line):
  parts = line.split()
  
  for i in range(len(parts)):
    # format txt
    if parts[i].startswith("user="):
      user = parts[i].split("=") [1]
      return user
    #format ssh.log
    elif parts[i] == "for":
      if i + 1 < len(parts):
        if parts[i + 1] != "invalid":
          user = parts[i + 1]
          return user
    elif parts[i] == "invalid":
      if i + 2 < len(parts):
        if parts[i + 1] == "user":
          user = parts[i + 2]
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

#functio qui compte les fails par user
def count_fail_by_user(parsed_logs):
  fail_by_user = {}
  
  for log in parsed_logs:
    if log["user"] is not None:
      if log["status"] == "FAIL":
        if log["user"] not in fail_by_user:
          fail_by_user[log["user"]] = 1
        else:
          fail_by_user[log["user"]] += 1
  
  return fail_by_user

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

#function qui parse toutes les lineS et qui les met dans la liste parsed_logs dans main
def parse_log_lines(lines):
  parsed_logs = [] #liste qui sert de bd ou je stock les lines parsé
  
  for line in lines:
    parsed = parse_log_line(line)
    if parsed is not None:
      parsed_logs.append(parsed)
  
  return parsed_logs