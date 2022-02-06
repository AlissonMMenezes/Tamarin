import subprocess
import yaml
import threading


with open("example.yaml", "r") as f:
    vms = yaml.load(f.read(),Loader=yaml.FullLoader)

print(vms)
for vm in vms["vms"]:    
    params = []
    params.append("/opt/homebrew/bin/qemu-system-x86_64")
    params.append("-m %s"%vm["memory"])
    port_forward = ""
    for p in vm["port-forward"]:
        print(p)
        host_port, guest_port = p.split(":")
        port_forward += ",hostfwd=tcp::{0}-:{1}".format(host_port,guest_port)
    params.append("-nic user,id=net0"+port_forward)
    params.append("-drive file=/Users/alissonmachado/Documents/GitHub/Tamarin/disk2.qcow2")
    print(params)    
    output = subprocess.Popen([" ".join(params)],stdout=subprocess.PIPE,shell=True).communicate()[0]
    print(output)
    break
