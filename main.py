def read_log(path):
  with open(path) as file:
      lines = file.readlines()
    
  clean_lines = []
    
  for line in lines:
      clean_lines.append(line.strip())

  return clean_lines

file_path = input("Entrez le nom du fichier a analyser : ")
lines = read_log(file_path)


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

result = count_status(lines)

def show_summary(result, file_path):
  print("===== Résumé LogGuard =====")
  print(f"===== Nom du fichier : {file_path} =====")
  print("SUCCESS :", result["success"])
  print("FAIL :", result["fail"])
  print("===================================")

show_summary(result, file_path)