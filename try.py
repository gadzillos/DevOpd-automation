import os

os.system("sudo yum update")
os.system("sudo yum install dnf")
os.system("sudo yum install wget unzip")

#Azure installation
os.system("sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc")
os.system("""echo -e "[azure-cli]
name=Azure CLI
baseurl=https://packages.microsoft.com/yumrepos/azure-cli
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo""")
os.system("sudo dnf install azure-cli")
os.system("az login")

answer ="0"
while answer != "y":
	os.system("echo Continue? Press y when logged in.")
	answer = raw_input()

#terraform launch
os.system("wget https://releases.hashicorp.com/terraform/1.0.11/terraform_1.0.11_linux_amd64.zip")
os.system("sudo unzip ./terraform_1.0.11_linux_amd64.zip -d /usr/local/bin/")
os.system("terraform -v")


import os
os.chdir("/home/centos/Downloads/repo-python/Terraform")
os.system("terraform init")
os.system("terraform validate")
os.system("terraform apply")
