import yaml

# Чтение YAML-файла
with open("config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

print(config_data) 
