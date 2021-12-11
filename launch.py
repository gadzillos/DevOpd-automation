import os
import subprocess
import argparse
import codecs
import json
import shutil


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

# os.system("sudo yum -y update")
os.system("sudo yum -y install dnf")
os.system("sudo yum -y install wget unzip")

# Download and unzip terraform to bin
os.chdir(os.path.expanduser('~'))
os.system("wget https://releases.hashicorp.com/terraform/1.0.11/terraform_1.0.11_linux_amd64.zip")
os.system("sudo unzip ./terraform_1.0.11_linux_amd64.zip -d /usr/local/bin/")
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
    with open('../VM1privateip.txt') as f:
        ip1 = f.read()
    
    inventory = (f"[jenkins_node]\n" + f"{ip2} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM2.pem\n\n" +
                 f"[docker_node]\n" + f"{ip1} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM1.pem\n\n" +
                 f"[wildfly_node]\n" + f"{ip3} ansible_user=azureuser ansible_ssh_private_key_file=../sshVM3.pem\n\n")

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
os.system("touch known_hosts")
os.system(f"ssh-keyscan -H {ip2} >> ~/.ssh/known_hosts")

#Ansible installation
terminal_message("Updating system")
os.system("sudo yum update -y")
os.system("sudo yum install -y python3-pip")
os.system("sudo pip3 install --upgrade pip")

terminal_message("Installing Ansible")
os.system("pip3 install 'ansible==2.9.17'")

terminal_message("Installing git. Clone")
os.system("ansible --version")
os.system("sudo yum -y install git")
os.system("git --version")

# send tar archive to VM2
terminal_message("sending tar file to VM")
os.chdir(original_path)
os.system(f"tar -cf repo.tar . &&" + 
          f"rsync --rsh='ssh -i sshVM2.pem' repo.tar azureuser@{ip2}:~")

# Ansible playbook start
os.chdir(original_path + "/Ansible")
os.system("ansible-playbook -i inventory setup.yml")
os.system("ansible-playbook -i inventory plugin.yml")