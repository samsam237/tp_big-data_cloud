import json
import os
from src.deploy_ova import deploy_ova
from src.clone_vm import clone_vm
from src.create_vm import create_vm
from src.connect import simple_connect, disconnect


if __name__ == "__main__":
    config_file = '../conf/config.json'
    
    if not os.path.exists(config_file):
        print(f"Le fichier de configuration {config_file} est introuvable.")
        exit (1)

    with open(config_file) as f:
        config = json.load(f)

    # Connexion au vCenter
    si = simple_connect(config['vcenter'], config['username'], config['password'])
    if not si:
        print("Échec de la connexion au vCenter.")
        exit (1)

    content = si.RetrieveContent()

    # Déploiement des OVAs
    print("Début du déploiement des VMs...")
    for vm in config['vms']:
        deploy_ova(vm['path'], vm['name'], vm['State'], content)

    # Clonage des VMs
    print("Début du clonage des VMs...")
    for clone in config['clones']:
        clone_vm(clone['template'], clone['name'], content)

    # Création de VMs from scratch
    print("Début de la création des VMs from scratch...")
    for vm in config['create_from_scratch']:
        create_vm(vm['name'], vm['ram'], vm['disk_size'], vm['Guest'], content, vm['State'])

    # Déconnexion
    disconnect(si)
    print("Processus terminé.")
