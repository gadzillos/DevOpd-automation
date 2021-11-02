# Create Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# Create virtual network
resource "azurerm_virtual_network" "myterraformnetwork" {
  name                = "myVnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name

  tags = {
    environment = local.environment
  }
}

# Create subnet
resource "azurerm_subnet" "myterraformsubnet" {
  name                 = "mySubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.myterraformnetwork.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create public IPs
resource "azurerm_public_ip" "VM3_public_ip" {
  name                = "myPublicIP3"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"

  tags = {
    environment = local.environment
  }
}
output "ip_3" {
  value = azurerm_public_ip.VM3_public_ip.ip_address
}

resource "azurerm_public_ip" "VM2_public_ip" {
  name                = "myPublicIP2"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"

  tags = {
    environment = local.environment
  }
}
output "ip_2" {
  value = azurerm_public_ip.VM2_public_ip.ip_address
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "myterraformnsg" {
  name                = "NSG"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    environment = local.environment
  }
}

# Create network interface
resource "azurerm_network_interface" "Nic1" {
  name                = "Nic1"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "nicConfig1"
    subnet_id                     = azurerm_subnet.myterraformsubnet.id
    private_ip_address_allocation = "Dynamic"
  }

  tags = {
    environment = local.environment
  }
}

resource "azurerm_network_interface" "Nic2" {
  name                = "Nic2"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "nicConfig2"
    subnet_id                     = azurerm_subnet.myterraformsubnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.VM2_public_ip.id
  }

  tags = {
    environment = local.environment
  }
}

resource "azurerm_network_interface" "Nic3" {
  name                = "Nic3"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "nicConfig3"
    subnet_id                     = azurerm_subnet.myterraformsubnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.VM3_public_ip.id
  }

  tags = {
    environment = local.environment
  }
}

# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "nsga1" {
  network_interface_id      = azurerm_network_interface.Nic1.id
  network_security_group_id = azurerm_network_security_group.myterraformnsg.id
}

resource "azurerm_network_interface_security_group_association" "nsga2" {
  network_interface_id      = azurerm_network_interface.Nic2.id
  network_security_group_id = azurerm_network_security_group.myterraformnsg.id
}

resource "azurerm_network_interface_security_group_association" "nsga3" {
  network_interface_id      = azurerm_network_interface.Nic3.id
  network_security_group_id = azurerm_network_security_group.myterraformnsg.id
}

# Generate random text for a unique storage account name
resource "random_id" "randomId" {
  keepers = {
    # Generate a new ID only when a new resource group is defined
    resource_group = azurerm_resource_group.rg.name
  }

  byte_length = 8
}

# Create storage account for boot diagnostics
resource "azurerm_storage_account" "mystorageaccount" {
  name                     = "diag${random_id.randomId.hex}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = local.environment
  }
}

# Create (and display) an SSH key
resource "tls_private_key" "ssh_1" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
output "tls_private_key_1" {
  value     = tls_private_key.ssh_1.private_key_pem
  sensitive = true
}

# Create (and display) an SSH key
resource "tls_private_key" "ssh_2" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
output "tls_private_key_2" {
  value     = tls_private_key.ssh_2.private_key_pem
  sensitive = true
}

# Create (and display) an SSH key
resource "tls_private_key" "ssh_3" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
output "tls_private_key_3" {
  value     = tls_private_key.ssh_3.private_key_pem
  sensitive = true
}

# Create virtual machine 1
resource "azurerm_linux_virtual_machine" "myterraformvm_1" {
  name                  = "VM_1"
  location              = var.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.Nic1.id]
  size                  = "Standard_B1s"

  os_disk {
    name                 = "VM1disk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "OpenLogic"
    offer     = "CentOS"
    sku       = "7_9-gen2"
    version   = "latest"
  }

  computer_name                   = "VM1"
  admin_username                  = "azureuser"
  disable_password_authentication = true

  admin_ssh_key {
    username   = "azureuser"
    public_key = tls_private_key.ssh_1.public_key_openssh
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.mystorageaccount.primary_blob_endpoint
  }

  tags = {
    environment = local.environment
  }
}

# Create virtual machine 2
resource "azurerm_linux_virtual_machine" "myterraformvm_2" {
  name                  = "VM_2"
  location              = var.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.Nic2.id]
  size                  = "Standard_B1s"

  os_disk {
    name                 = "VM2disk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "OpenLogic"
    offer     = "CentOS"
    sku       = "7_9-gen2"
    version   = "latest"
  }

  computer_name                   = "VM2"
  admin_username                  = "azureuser"
  disable_password_authentication = true

  admin_ssh_key {
    username   = "azureuser"
    public_key = tls_private_key.ssh_2.public_key_openssh
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.mystorageaccount.primary_blob_endpoint
  }

  tags = {
    environment = local.environment
  }
}

# Create virtual machine 3
resource "azurerm_linux_virtual_machine" "myterraformvm_3" {
  name                  = "VM_3"
  location              = var.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.Nic3.id]
  size                  = "Standard_B1s"

  os_disk {
    name                 = "VM3disk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "OpenLogic"
    offer     = "CentOS"
    sku       = "7_9-gen2"
    version   = "latest"
  }

  computer_name                   = "VM3"
  admin_username                  = "azureuser"
  disable_password_authentication = true

  admin_ssh_key {
    username   = "azureuser"
    public_key = tls_private_key.ssh_3.public_key_openssh
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.mystorageaccount.primary_blob_endpoint
  }

  tags = {
    environment = local.environment
  }
}

resource "local_file" "pem_file2" {
  filename             = pathexpand("../sshVM2.pem")
  file_permission      = "600"
  directory_permission = "700"
  sensitive_content    = tls_private_key.ssh_2.private_key_pem
}

resource "local_file" "pem_file3" {
  filename             = pathexpand("../sshVM3.pem")
  file_permission      = "600"
  directory_permission = "700"
  sensitive_content    = tls_private_key.ssh_3.private_key_pem
}

resource "local_file" "VM2publicip_file" {
  filename             = pathexpand("../VM2publicip.txt")
  file_permission      = "600"
  directory_permission = "700"
  content              = azurerm_public_ip.VM2_public_ip.ip_address
}

resource "local_file" "VM3publicip_file" {
  filename             = pathexpand("../VM3publicip.txt")
  file_permission      = "600"
  directory_permission = "700"
  content              = azurerm_public_ip.VM3_public_ip.ip_address
}