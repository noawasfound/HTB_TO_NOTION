import requests
from notion_client import Client

# 🔑 API Notion
NOTION_API_KEY = "ntn_O85574266691LMRWYk2Q4EP04yUps5GD052G30Os0qa3Tq"
DATABASE_ID_MACHINES = "1951fe0ff7ed80fa9c43e215a63e2ba3"
DATABASE_ID_MODULES = "1951fe0ff7ed806380eac905fe70426e"

notion = Client(auth=NOTION_API_KEY)

# 🔐 Credentials HTB
HTB_USERNAME = "noalbd"
HTB_EMAIL = "noalabuda@gmail.com"
HTB_PASSWORD = "ZDThr9sD6UeCp9f*"

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
