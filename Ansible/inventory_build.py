import os

ip1, ip2, ip3 = "", "", ""

with open('../VM2publicip.txt') as f:
    ip2 = f.read()
with open('../VM3publicip.txt') as f:
    ip3 = f.read()    
with open('../VM1privateip.txt') as f:
    ip1 = f.read()
    
inventory = (f"[jenkins_node]\n" + f"{ip2} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM2.pem\n\n" +
             f"[docker_node]\n" + f"{ip1} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM1.pem\n\n" +
             f"[wildfly_node]\n" + f"{ip3} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM3.pem\n\n")

with open('inventory', 'w') as f:
    f.writelines(inventory)
