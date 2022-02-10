import subprocess
import yaml
import threading
import paramiko
import socket
import time
import sys
from terminaltables import AsciiTable
import os
import shutil

qemu_bin = shutil.which("qemu-system-x86_64")
if not os.path.exists(".data"): os.mkdir(".data")


class VirtualMachine:
    def __init__():
        pass
        
class Tamarin:
    def __init__():
        pass

def help():
    print("""
    Usage:
    tamarin.py [provision|destroy]
    tamarin.py start [vm_name]
    tamarin.py stop [vm_name]
    tamarin.py destroy [vm_name]
    tamarin.py list
    tamarin.py help
    """)

def parse_yaml(file_name="Inventory.yml"):
    with open(file_name, "r") as f:
        inventory = yaml.load(f.read(),Loader=yaml.FullLoader)
    return inventory

def list_vms():
    inventory = parse_yaml()
    table_data = [
            ['Name', 'status'],
        ]
    for vm in inventory["inventory"]["vms"]:
        status = "Running" if os.path.exists(".data/{0}.pid".format(vm["name"])) else "Stopped"
        table_data.append([vm["name"], status])
    
    table = AsciiTable(table_data)
    print (table.table)

def create_vm(vm):
    print("[+] Creating VM: {0}".format(vm["name"]))
    params = []
    params.append("{0} --nographic --pidfile .data/{1}.pid".format(qemu_bin, vm["name"]))
    params.append("-m %s"%vm["memory"])
    port_forward = ""
    for p in vm["port-forward"]:
        host_port, guest_port = p.split(":")
        port_forward += ",hostfwd=tcp::{0}-:{1}".format(host_port,guest_port)
    params.append("-nic user,id=net0"+port_forward)
    params.append("-drive file=/Users/alissonmachado/Documents/GitHub/Tamarin/disk2.qcow2")
    output = subprocess.Popen([" ".join(params)],stdout=subprocess.PIPE,shell=True)
    for p in vm["port-forward"]:
        host_port, guest_port = p.split(":")
        if int(guest_port) == 22:
            provisioning(vm, host_port)
            break

def provisioning(vm,ssh_port):
    while True:
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = ("127.0.0.1", int(ssh_port))
        result_of_check = a_socket.connect_ex(location)
        if result_of_check == 0:
            a_socket.close()
            print("[+] VM Started!")
            i = 0
            while i < 3:
                try: 
                    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    a_socket.connect(location)
                    banner = a_socket.recv(100)
                    if "SSH" in str(banner):
                        print("[+] VM Ready!")
                        break
                    else:
                        time.sleep(10)                  
                except Exception as e:
                    print(e)
                    time.sleep(10)
                i += 1
            break
        else:
            print("[+] Waiting the VM to start")    
            time.sleep(35) 

    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='127.0.0.1',port=ssh_port,username='root',password='alisson')
        stdin,stdout,stderr = ssh.exec_command("touch /file_provisioned.txt")
        if stderr.channel.recv_exit_status() != 0:
            stderr.read()
        else:
            stdout.read()
    except Exception as e:
        print("[+] Waiting for an ssh connection")            


def menu():
    if len(sys.argv) < 2:
        help()
    elif sys.argv[1] == "start":
        if len(sys.argv) > 2:
            for vm in parse_yaml()["inventory"]["vms"]:
                if vm["name"] == sys.argv[2]:
                    t = threading.Thread(target=create_vm,args=(vm,))
                    t.start()
                    while t.is_alive():
                        time.sleep(5)
                    t.join()
                    break            
            
        else:
            print("[+] Provisioning VMs")
            for vm in parse_yaml()["inventory"]["vms"]: 
                t = threading.Thread(target=create_vm,args=(vm,))
                t.start()
                while t.is_alive():
                    time.sleep(5)
                t.join()
    elif sys.argv[1] == "stop":
        with open(".data/{0}.pid".format(sys.argv[2])) as f:
            pid = int(f.read())
            os.kill(pid, 1)
            print("[!] Shutting down VM: {0}".format(sys.argv[2]))
    elif sys.argv[1] == "destroy":
        with open(".data/{0}.pid".format(sys.argv[2])) as f:
            pid = f.read()
            print("[!] Shutting down VM: {0}".format(sys.argv[2]))
    elif sys.argv[1] == "list":
        list_vms()
    else:
        #os.mkdir(".data")
        pass   

if __name__ == "__main__":
    menu()    