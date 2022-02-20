# Tamarin
![alt text](img/tamarin.png) IaC made in Python

This is a python tool to provide virtual machines on any operating systems.

It was created initally to replace vagrant for the Mac M1, once the VirtualBox is not compatible with this new processor.


## Installation

    brew install qemu
    python3 -m pip install tamarin

## How to use it

First create a file called inventory.yml

Example:
    inventory:
        image: debian
        ssh-user: root
        ssh-password: alisson
        vms:
            - name: webserver
              memory: 512
              address: 192.168.55.10/24
              port-forward:
                - "4022:22"
                - "8080:80"
              provision_script: setup_webserver.sh    

Then you can check your iventory using:

    $ tamarin status

    +-----------+---------+
    | Name      | status  |
    +-----------+---------+
    | webserver | Stopped |
    | database  | Stopped |
    +-----------+---------+

Run your VM:
    $ tamarin start webserver
    [+] Creating VM: webserver
    [+] Setting up VM: webserver on port 4022
    [!] Waiting port 4022 to be open
    [+] VM Ready!
    [+] Setting the hostname

Access via ssh:
    (base) alissonmachado@Alissons-Air Tamarin % ssh root@localhost -p 4022
    root@localhost's password: 
    
    Linux webserver 5.10.0-11-amd64 #1 SMP Debian 5.10.92-1 (2022-01-18) x86_64
    root@webserver:~# 


