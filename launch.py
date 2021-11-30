import os

script_path = os.getcwd()

script_path += "/Terraform"

#os.system("sudo yum -y update")
os.system("sudo yum -y install dnf")
os.system("sudo yum -y install wget unzip")

#Download and unzip terraform to bin
os.chdir(os.path.expanduser('~'))
os.system("wget https://releases.hashicorp.com/terraform/1.0.11/terraform_1.0.11_linux_amd64.zip")
os.system("sudo unzip ./terraform_1.0.11_linux_amd64.zip -d /usr/local/bin/")
os.system("terraform -v")

#Azure installation
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

answer ="0"
while not ((answer == "1") or (answer == "2") or (answer == "3")):
    os.system("\n")
    answer = raw_input("Type in option number: ")

if answer == '1':
    login = raw_input("Type in your login: ")
    password = raw_input("Type in your password: ")
    os.system("az login -u " + login + " -p "+ password)
elif answer == '3':
    os.system("az login")
else:
    appID = raw_input("Type in your app-id: ")
    password = raw_input("Type in your password/cert: ")
    tenant = raw_input("Type in tenant: ")
    os.system("az login --service-principal -u "+ appID +" -p "+ password +" --tenant "+ tenant)

#terraform launch
import os
os.chdir(script_path)
os.system("terraform init")
os.system("terraform validate")
os.system("terraform apply")
