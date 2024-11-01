import json
from connect import simple_connect, disconnect
from pyVmomi import vim
from pyVim import connect

def clone_vm(template_name, new_vm_name, content):
    template_vm = content.searchIndex.FindByDnsName(None, template_name, True)
    if not template_vm:
        print(f"Template {template_name} introuvable.")
        return

    clone_spec = vim.vm.CloneSpec(powerOn=False, template=False)
    task = template_vm.Clone(folder=template_vm.parent, name=new_vm_name, spec=clone_spec)
    print(f"Clonage de {template_name} en {new_vm_name} en cours...")
    connect.WaitForTask(task)
    
    new_vm = content.searchIndex.FindByDnsName(None, new_vm_name, True)
    if new_vm:
        if clone_spec.powerOn:
            task = new_vm.PowerOn()
            connect.WaitForTask(task)
    
    print(f"{new_vm_name} clonée avec succès.")

if __name__ == "__main__":
    config_file = '../conf/config.json'
    with open(config_file) as f:
        config = json.load(f)

    si = simple_connect(config['vcenter'], config['username'], config['password'])
    content = si.RetrieveContent()

    for clone in config['clones']:
        clone_vm(clone['template'], clone['name'], content)

    disconnect(si)
