#fonction qui lis le fichier mis en path
def read_log(path):
  with open(path) as file:
      lines = file.readlines()
    
  clean_lines = []
    
  for line in lines:
      clean_lines.append(line.strip())
      
  return clean_lines

#fonction qui fait le compte des status de connexion
def count_status(lines):
  success = 0
  fail = 0
  
  for line in lines:
    if "SUCCESS" in line:
      success += 1
    if "FAIL" in line:
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

#function qui compte les tentative fail de co d'une ip
def is_suspicious(count, threshold):
  if count >= threshold:
    return True
  else:
    return False

#function qui compte le nombre fail par IP
def count_fail_by_ip(lines):
  fail_by_ip = {}
  
  for line in lines:
    if "FAIL" in line:
      ip = extract_ip(line)
      
      if ip not in fail_by_ip:
        fail_by_ip[ip] = 1
      else:
        fail_by_ip[ip] += 1
        
  return fail_by_ip

#function qui stock les IP suspectes
def get_suspicious_ips(fail_by_ip, threshold):
  suspicious_ips = []
  
  for ip, count in fail_by_ip.items():
    if is_suspicious(count, threshold):
      suspicious_ips.append(ip)
        
  return suspicious_ips