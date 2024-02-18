import os
from tqdm import tqdm
from chains import Chains
import json
Chains.setLlm()

folder_path = "/home/melih/Downloads/Alogia english/Alogia english/Alogia services/"

all_services = {}
index = 0
for filename in tqdm(os.listdir(folder_path)):
    path = os.path.join(folder_path, filename)
    service_name = path.split("/")[-1].split(".")[0]
    service_name = " ".join(service_name.split()[:-1])
    explanation = Chains.intro(path)
    all_services[service_name] = explanation
    print(service_name, explanation)
    
# Convert all_services to JSON
services_json = json.dumps(all_services, indent=4)

# Save JSON to a file
with open("services.json", "w") as f:
    f.write(services_json)
