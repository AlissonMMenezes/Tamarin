import subprocess
import yaml
import threading
import paramiko
import socket
import time

with open("example.yaml", "r") as f:
    vms = yaml.load(f.read(),Loader=yaml.FullLoader)

print(vms)
def create_vm(vm):
    print("Creating VM: {}".format(vm["name"]))
    params = []
    params.append("/opt/homebrew/bin/qemu-system-x86_64 -nographic")
    params.append("-m %s"%vm["memory"])
    port_forward = ""
    for p in vm["port-forward"]:
        print(p)
        host_port, guest_port = p.split(":")
        port_forward += ",hostfwd=tcp::{0}-:{1}".format(host_port,guest_port)
    params.append("-nic user,id=net0"+port_forward)
    params.append("-drive file=/Users/alissonmachado/Documents/GitHub/Tamarin/disk2.qcow2")
    print(params)        
    output = subprocess.Popen([" ".join(params)],stdout=subprocess.PIPE,shell=True)
    print(output)

def provisioning(vm):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='127.0.0.1',port=2222,username='root',password='alisson')
    stdin,stdout,stderr = ssh.exec_command("touch /file_provisioned.txt")
    if stderr.channel.recv_exit_status() != 0:
        print(stderr.read())
    else:
        print(stdout.read())

for vm in vms["vms"]:   
    t = threading.Thread(target=create_vm,args=(vm,))
    t.start()
    while True:
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = ("127.0.0.1", 2222)
        result_of_check = a_socket.connect_ex(location)
        if result_of_check == 0:
            print("[+] VM Started!")    
            break
        else:
            print("[+] Waiting the VM to start")    
            time.sleep(35)        
    provisioning(vm)
    t.join()
    break

