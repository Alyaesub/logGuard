import socket
import requests

# function qui vérifie si un port est ouvert via l'ip
def check_port(ip,port):
  #créé le socket coter client
  socket_scann = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  socket_scann.settimeout(1)
  #Connexion au server via l'ip et le port
  response = socket_scann.connect_ex((ip, port))
  
  socket_scann.close()
  
  if response == 0:
    return True
  else:
    return False

# finction qui scann les ports d'une IP
def scan_ports(ip, ports):
  port_results = {}
  
  for port in ports:
    ports_scanned = check_port(ip,port)
    port_results[port] = ports_scanned
  
  return port_results

#function qui scanne les suspicious_ip
def scan_suspicious_ips(suspicious_ips, ports):
  suspicious_ips_scanned = {}
  
  for ip in suspicious_ips:
    result = scan_ports(ip, ports)
    suspicious_ips_scanned[ip] = result
  
  return suspicious_ips_scanned


# function qui sert a reverse DNS de l'ip
def resolve_hostname(ip):
  try:
    result = socket.gethostbyaddr(ip)
    hostname = result[0]
    return hostname
  except socket.error :
    return None

#function qui revers DNS les ips suspecte
def reverse_dns_suspicious_ips(suspicious_ips):
  suspicious_ips_resolved = {}
  
  for ip in suspicious_ips:
    result = resolve_hostname(ip)
    suspicious_ips_resolved[ip] = result
  
  return suspicious_ips_resolved

# function qui envoie une requete http sur un port ouvert
def check_http(ip, port):
  if port == 80:
    url = f"http://{ip}"
  elif port == 443:
    url = f"https://{ip}"
  else:
    return {
      "reachable": False,
      "status_code": None
      }
  
  try: 
    response = requests.get(url, timeout=3)
    return {
      "reachable": True,
      "status_code": response.status_code,
    }
  except requests.RequestException:
    return {
      "reachable": False,
      "status_code": None,
      }

#function qui envoie des requetes http sur les IPS suspectes
def check_http_suspicious_ips(scanned_suspicious_ips):
  request_suspicious_ips = {}
  
  for ip, ports in scanned_suspicious_ips.items():
    http_results = {}
    
    for port, is_open in ports.items():
      if is_open:
        if port in [80, 443]:
          result = check_http(ip,port)
          http_results[port] = result
    
    request_suspicious_ips[ip] = http_results
  
  return request_suspicious_ips