
import yaml



def load_data(file_path:str)->list|dict:
    with open(file_path, encoding="utf-8") as f:
        data = yaml.load(f.read(), yaml.Loader) #Also works with json files
    return data

def save_data(data:dict|list, file_path:str):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(yaml.dump(data, allow_unicode=True, default_style="'"))
