import requests
import os
from dotenv import load_dotenv
from notion_client import Client

# Charger les variables d'environnement
load_dotenv()

# API Notion
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID_MACHINES = os.getenv("DATABASE_ID_MACHINES")
DATABASE_ID_MODULES = os.getenv("DATABASE_ID_MODULES")

notion = Client(auth=NOTION_API_KEY)

# Credentials HTB
HTB_USERNAME = os.getenv("HTB_USERNAME")
HTB_EMAIL = os.getenv("HTB_EMAIL")
HTB_PASSWORD = os.getenv("HTB_PASSWORD")

session = requests.Session()

# 🔄 1️⃣ Connexion à HTB Academy
def login_htb():
    url = "https://academy.hackthebox.com/api/v1/login"
    data = {"email": HTB_EMAIL, "password": HTB_PASSWORD}
    response = session.post(url, json=data)
    return response.status_code == 200

# 🔄 2️⃣ Récupérer les machines HTB complétées
def get_htb_machines():
    url = f"https://www.hackthebox.com/api/v4/profile/{HTB_USERNAME}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["profile"]["owned_boxes"]
    return []

# 🔄 3️⃣ Récupérer les modules HTB Academy
def get_academy_modules():
    url = "https://academy.hackthebox.com/api/v1/module/progress"
    response = session.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    return []

# 📤 4️⃣ Envoyer une machine à Notion
def add_machine_to_notion(machine_name, difficulty, status):
    notion.pages.create(
        parent={"database_id": DATABASE_ID_MACHINES},
        properties={
            "Nom": {"title": [{"text": {"content": machine_name}}]},
            "Difficulté": {"select": {"name": difficulty}},
            "Statut": {"select": {"name": status}}
        }
    )

# 📤 5️⃣ Envoyer un module à Notion
def add_module_to_notion(module_name, difficulty, status, progress):
    notion.pages.create(
        parent={"database_id": DATABASE_ID_MODULES},
        properties={
            "Nom": {"title": [{"text": {"content": module_name}}]},
            "Difficulté": {"select": {"name": difficulty}},
            "Statut": {"select": {"name": status}},
            "Progression": {"number": progress}
        }
    )

# 🚀 6️⃣ Exécution
if login_htb():
    print("✅ Connecté à HTB Academy !")

    # Récupérer et envoyer les machines
    machines = get_htb_machines()
    for machine in machines:
        add_machine_to_notion(machine["name"], machine["difficulty"], "Complété")
    
    print("✅ Machines envoyées à Notion !")

    # Récupérer et envoyer les modules
    modules = get_academy_modules()
    for module in modules:
        name = module["module"]["name"]
        difficulty = module["module"]["difficulty"]
        status = "Complété" if module["completed"] else "En cours"
        progress = module["progress"]
        
        add_module_to_notion(name, difficulty, status, progress)

    print("✅ Modules envoyés à Notion !")
