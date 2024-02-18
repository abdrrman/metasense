import json

with open("tree_based_data.json") as f:
    tree_based_data = json.load(f)
    
with open("services.json") as f:
    services = json.load(f)

"""service_names = set(services.keys())

tree_services = set()
for cat, data in tree_based_data.items():
    tree_services |= set(data["services"])

print(service_names - tree_services)"""

category_input = "Categories:\n\n"
for category, data in tree_based_data.items():
    category_input += f"Category Name: {category}\n"
    category_input += f"Category Description: {data['generated_description']}\n"
    category_input += "\n"*2 + "#"*50+"\n"*2

print(category_input)

