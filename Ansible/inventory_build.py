import os

ip1, ip2, ip3 = "", "", ""

with open('../VM2publicip.txt') as f:
    ip2 = f.read()
with open('../VM3publicip.txt') as f:
    ip3 = f.read()    
with open('../VM1privateip.txt') as f:
    ip1 = f.read()
    
inventory = (f"[jenkins_node]\n" + f"{ip2} ansible_ssh_user=azureuser ansible_ssh_private_key=/sshVM2.pem\n\n" +
             f"[docker_node]\n" + f"{ip1} ansible_ssh_user=azureuser ansible_ssh_private_key=/sshVM1.pem\n\n" +
             f"[wildfly_node]\n" + f"{ip3} ansible_ssh_user=azureuser ansible_ssh_private_key=/sshVM3.pem\n\n")

with open('inventory', 'w') as f:
    f.writelines(inventory)
#os.system(f"export Inventory={inventory}")
#os.system(f"sudo echo {inventory} > inventory")