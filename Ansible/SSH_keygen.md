SSH-key connection instruction:  
$ ssh-keygen -t rsa  
$ ssh-copy-id -i $HOME/.ssh/id_rsa.pub root@<remote_ip>  
$ ssh root@<remote_ip>  
