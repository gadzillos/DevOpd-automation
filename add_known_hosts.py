import os

ip1, ip3 = "", ""

with open('VM3publicip.txt') as f:
    ip3 = f.read()    
with open('VM1privateip.txt') as f:
    ip1 = f.read()

os.system("sudo touch ~/.ssh/known_hosts")
os.system(f"ssh-keyscan -H {ip1} >> ~/.ssh/known_hosts")
os.system(f"ssh-keyscan -H {ip3} >> ~/.ssh/known_hosts")