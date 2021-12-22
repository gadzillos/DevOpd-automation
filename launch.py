import os
import subprocess
import argparse
import codecs
import json
import shutil
import secrets
import yaml


def terminal_message(message):
    cyan = "\033[0;36m"
    no_color = "\033[0m"
    (columns, lines) = shutil.get_terminal_size()
    fill_line = ""
    for i in range(columns):
        fill_line += "~"
    os.system(f"echo && echo -e '{cyan}{fill_line}' && echo")
    os.system(f"echo -e '{cyan}{message}'")
    os.system(f"echo -e '{cyan}{fill_line}{no_color}' && echo")
    
    
#parsing file with login to Azure
parser = argparse.ArgumentParser()
parser.add_argument('-p','--path', help='implement path to login file')
args= parser.parse_args()

script_path = os.getcwd()
original_path = script_path
script_path += "/Terraform"

# fix time issues for terraform
os.system("sudo yum -y install ntp")
os.system("sudo timedatectl set-ntp true")
os.system("timedatectl")

# os.system("sudo yum -y update")
os.system("sudo yum -y install dnf")
os.system("sudo yum -y install wget unzip")

# Download and unzip terraform to bin
os.chdir(os.path.expanduser('~'))
os.system("wget https://releases.hashicorp.com/terraform/1.1.0/terraform_1.1.0_linux_amd64.zip")
os.system("sudo unzip -u ./terraform_1.1.0_linux_amd64.zip -d /usr/local/bin/")
os.system("sudo rm -f terraform_1.1.0_linux_amd64.zip")
os.system("terraform -v")

# Azure installation
os.system("sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc")
os.system("""echo -e "[azure-cli]
name=Azure CLI
baseurl=https://packages.microsoft.com/yumrepos/azure-cli
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo""")
os.system("sudo dnf -y install azure-cli")
terminal_message("Installed azure-cli")


def login_and_terraform_apply(subscription_id, app_id, password_value, tenant_value):
    os.chdir(script_path)
    bash_command = (f"export ARM_SUBSCRIPTION_ID='{subscription_id}' && " +
                    f"export ARM_CLIENT_ID='{app_id}' && " +
                    f"export ARM_CLIENT_SECRET='{password_value}' && " +
                    f"export ARM_TENANT_ID='{tenant_value}' &&" +
                    f"az login --service-principal -u '{app_id}' -p '{password_value}' --tenant '{tenant_value}' &&" +
                    f"terraform init && terraform validate && terraform apply -auto-approve && echo done!")
    process = subprocess.run(bash_command, shell = True)
    

def inventory_build():
    os.chdir(original_path + "/Ansible")
    ip1, ip3 = "", ""
    global ip2

    ip1, ip2, ip3 = "", "", ""

    with open('../VM2publicip.txt') as f:
        ip2 = f.read()
    with open('../VM3publicip.txt') as f:
        ip3 = f.read()    
    with open('../VM1publicip.txt') as f:
        ip1 = f.read()
    
    inventory = (f"jenkins_node ansible_host={ip2} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM2.pem\n\n" +
                 f"docker_node ansible_host={ip1} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM1.pem\n\n" +
                 f"wildfly_node ansible_host={ip3} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM3.pem\n\n")

    with open('inventory', 'w') as f:
        f.writelines(inventory)


#login information passed to terraform
with open(args.path,'r') as f:	
	data= json.load(f)
app_ID = data['appId']
password = data['password']
tenant = data['tenant']
subscription_ID = data['subscriptionId']
login_and_terraform_apply(subscription_ID, app_ID, password, tenant)
terminal_message("Terraform applied")
    
# Ansible inventory build
inventory_build()
terminal_message("Inventory builded")

# Add VM2 to known_hosts for ssh connection
os.system("touch ~/.ssh/known_hosts")
os.system(f"ssh-keyscan -H {ip2} >> ~/.ssh/known_hosts")

#Ansible installation
terminal_message("Ansible installation")
os.system("sudo yum -y install ansible")

# send tar archive to VM2
terminal_message("sending tar file to VM")
os.chdir(original_path)
os.system(f"tar -cf repo.tar . &&" + 
          f"rsync --rsh='ssh -i sshVM2.pem' repo.tar azureuser@{ip2}:~ && echo 'rsync done'")
os.system("sudo rm -f repo.tar")

# Create password for Ansible Vault
os.chdir(original_path + "/Ansible")
password_length = 12
password = secrets.token_urlsafe(password_length)

with open("vault_password.txt", "w") as file:
    file.write(password)
with open("vault_password.yaml", "w") as file:
    file.write(yaml.safe_dump({'vault_password': password}))

# os.chdir(original_path + "/Ansible")
# subprocess.run(
#         "ansible-vault encrypt --vault-password-file"
#         " vault_password.txt credentials.yaml",
#         shell=True)


# Ansible playbook start --extra-vars '@credentials.yaml'
terminal_message("Starting ansilbe jenkins_node_preparation.yml on VM2")
os.chdir(original_path + "/Ansible")
os.system(f"ansible-playbook -v -i inventory jenkins_node_preparation.yml " +
          f"--vault-password-file vault_password.txt --extra-vars '@vault_password.yaml' --extra-vars 'credentials.yaml'")
