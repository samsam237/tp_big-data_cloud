import json
from connect import simple_connect, disconnect
from pyVmomi import vim
from pyVim import connect

def deploy_ova(ova_path, vm_name, guest_os, content):
    ovf_manager = content.ovfManager
    with open(ova_path, 'rb') as ovf_file:
        ovf_descriptor = ovf_file.read()

    import_spec = ovf_manager.CreateImportSpec(ovf_descriptor, resource_pool, datastore)
    if import_spec.error:
        print(f"- Erreur dans la création de l'import spec: {import_spec.error}")
        return

    task = ovf_manager.ImportVApp(import_spec, resource_pool, datastore)
    print(f"- Importation en cours pour {vm_name}...")
    connect.WaitForTask(task)
    
    vm = content.searchIndex.FindByDnsName(None, vm_name, True)
    if vm:
        if guest_os == "poweredOn":
            task = vm.PowerOn()
            connect.WaitForTask(task)
    
    print(f"{vm_name} déployée avec succès.")

if __name__ == "__main__":
    config_file = '../conf/config.json'
    with open(config_file) as f:
        config = json.load(f)

    si = simple_connect(config['vcenter'], config['username'], config['password'])
    content = si.RetrieveContent()

    resource_pool = content.viewManager.CreateContainerView(content.rootFolder, [vim.ResourcePool], True)[0]
    datastore = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True)[0]

    for vm in config['vms']:
        deploy_ova(vm['path'], vm['name'], vm['State'], content)

    disconnect(si)
