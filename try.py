import os
import subprocess

#installing repo
subprocess.run("cd",  "/etc")
subprocess.run("mkdir", "devop")
subprocess.run("cd", "/devop")
subprocess.run("git", "clone", "https://gitlab.com/devops_netcraker/repo.git")
)


#Azure installation
subprocess.run("rpm --import https://packages.microsoft.com/keys/microsoft.asc")
subprocess.run("echo", "-e", "[azure-cli]", "name=Azure CLI", "baseurl=https://packages.microsoft.com/yumrepos/azure-cli" ,"enabled=1", "gpgcheck=1", "gpgkey=https://packages.microsoft.com/keys/microsoft.asc", "sudo",  "tee", "/etc/yum.repos.d/azure-cli.repo")
subprocess.run("sudo", "dnf", "install",  "azure-cli")

#terraform launch
os.system("echo terraform init")
os.system("echo terraform validate")
os.system("echo terraform apply")