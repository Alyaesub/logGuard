import socket

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