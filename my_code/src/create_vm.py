import json
from connect import simple_connect, disconnect
from pyVmomi import vim
from pyVim import connect

def create_vm(vm_name, ram_mb, disk_size_gb, guest_os, content, state):
    resource_pool = content.viewManager.CreateContainerView(content.rootFolder, [vim.ResourcePool], True)[0]
    datastore = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True)[0]

    vm_spec = vim.vm.ConfigSpec()
    vm_spec.name = vm_name
    vm_spec.memoryMB = ram_mb
    vm_spec.numCPUs = 1
    vm_spec.guestId = guest_os  

    disk_spec = vim.vm.device.VirtualDisk()
    disk_spec.capacityInKB = disk_size_gb * 1024 * 1024
    disk_spec.backing = vim.vm.device.VirtualDiskFlatVer2BackingInfo()
    disk_spec.backing.diskMode = 'persistent'

    vm_spec.deviceChange = [vim.vm.device.DeviceChange(operation=vim.vm.device.DeviceChange.add, device=disk_spec)]

    task = resource_pool.CreateVM_Task(config=vm_spec, folder=resource_pool.parent)
    print(f"Création de la VM {vm_name} en cours...")
    connect.WaitForTask(task)

    new_vm = content.searchIndex.FindByDnsName(None, vm_name, True)
    if new_vm and state == "poweredOn":
        task = new_vm.PowerOn()
        connect.WaitForTask(task)

    print(f"{vm_name} créée avec succès.")

if __name__ == "__main__":
    config_file = '../conf/config.json'
    with open(config_file) as f:
        config = json.load(f)

    si = simple_connect(config['vcenter'], config['username'], config['password'])
    content = si.RetrieveContent()

    for vm in config['create_from_scratch']:
        create_vm(vm['name'], vm['ram'], vm['disk_size'], vm['Guest'], content, vm['State'])

    disconnect(si)
