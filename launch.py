import os
import subprocess

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

os.system("echo '\n~~~~~~~~~~\nChoose Azure login option:\n~~~~~~~~~~\n'")
os.system("echo '1: login -u <username> -p <password>\n'")
os.system("echo '2: service principal login <app-id> <password-or-cert> <tenant>\n'")
os.system("echo '3: login using browser\n'")


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

    with open('../VM2publicip.txt') as f:
        ip2 = f.read()
    with open('../VM3publicip.txt') as f:
        ip3 = f.read()    
    with open('../VM1privateip.txt') as f:
        ip1 = f.read()
    
    inventory = (f"[jenkins_node]\n" + f"{ip2} ansible_ssh_user=azureuser ansible_ssh_private_key=../sshVM2.pem\n\n" +
                 f"[docker_node]\n" + f"{ip1} ansible_ssh_user=azureuser ansible_ssh_private_key=../sshVM1.pem\n\n" +
                 f"[wildfly_node]\n" + f"{ip3} ansible_ssh_user=azureuser ansible_ssh_private_key=../sshVM3.pem\n\n")

    with open('inventory', 'w') as f:
        f.writelines(inventory)


appID = input("Type in your app-id: ")
password = input("Type in your password/cert: ")
tenant = input("Type in tenant: ")
subscription_ID = input("Type in your subscription ID: ")
login_and_terraform_apply(subscription_ID, appID, password, tenant)
    
# Ansible inventory build
inventory_build()

# Add VM2 to known_hosts for ssh connection
os.system(f"ssh-keyscan -H {ip2} >> ~/.ssh/known_hosts")

#Ansible installation
os.system("echo <-------- Updating system -------->")
os.system("sudo yum update -y")
os.system("sudo yum install -y python3-pip")
os.system("sudo pip3 install --upgrade pip")

os.system("echo <-------- Installing Ansible -------->")
os.system("pip3 install 'ansible==2.9.17'")

os.system("echo <-------- Installing git. Clone -------->")
os.system("ansible --version")
os.system("sudo yum -y install git")
os.system("git --version")

# send tar archive to VM2
os.chdir(original_path)
os.system(f"tar -cf repo.tar . &&" + 
          f"rsync --rsh='ssh -i sshVM2.pem' repo.tar azureuser@{ip2}:~")

# Ansible playbook start
os.chdir(original_path + "/Ansible")
os.system("ansible-playbook -i inventory setup.yml")
