---
title: terraform-to-create-Azure-linux-Virtual-Machine
description: terraform-to-create-Azure-linux-Virtual-Machine
date: 2022-12-11 22:33:16
tags: 
  - Terryform
  - Azure VM
categories:
  - Devops
---

## terraform-to-create-Azure-linux-Virtual-Machine

>  Reference

- https://github.com/hashicorp/terraform-provider-azurerm/tree/main/examples/virtual-machines

- https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-terraform

- https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_machine

- https://gmusumeci.medium.com/how-to-deploy-a-centos-linux-vm-in-azure-using-terraform-64d972008282



> install azure cli

https://learn.microsoft.com/zh-cn/cli/azure/install-azure-cli
> install terraform 

https://developer.hashicorp.com/terraform/downloads

> Get started
```hcl
[root@srv1 azure-vm]# cat output.tf
output "resource_group_name" {
  value = azurerm_resource_group.main.name
}
output "computer_name" {
  value = azurerm_linux_virtual_machine.main.computer_name
}
output "admin_username" {
  value = azurerm_linux_virtual_machine.main.admin_username
}
output "public_ip_address" {
  value = azurerm_linux_virtual_machine.main.public_ip_address
}
```
```hcl
[root@srv1 ~]# cat main.tf
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
    /* environment     = "public"
  subscription_id = var.azure-subscription-id
  client_id       = var.azure-client-id
  client_secret   = var.azure-client-secret
  tenant_id       = var.azure-tenant-id */
  }
}

resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-resources"
  location = var.location
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.prefix}-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "internal" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_public_ip" "main" {
  name                = "${var.prefix}-pip"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  allocation_method   = "Dynamic"
}

resource "azurerm_network_interface" "main" {
  name                = "${var.prefix}-nic"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.internal.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "nsg" {
  name                = "myNetworkSecurityGroup"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

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
}

# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "main" {
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

resource "azurerm_linux_virtual_machine" "main" {
  name                = "${var.prefix}-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B2s"
  admin_username      = "adminuser"
  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  source_image_reference {
    publisher = var.linux_vm_image_publisher
    offer     = var.linux_vm_image_offer
    sku       = var.centos_7_gen2_sku
    version   = "latest"
  }

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }

  os_disk {
    storage_account_type = "Standard_LRS"
    caching              = "ReadWrite"
  }
}
```
```hcl
[root@srv1 ~]# cat variables.tf
variable "prefix" {
  default     = "azvmlab"
  description = "The prefix which should be used for all resources in this example"
}

variable "location" {
  default     = "eastasia"
  description = "The Azure Region in which all resources in this example should be created."
}

# centos image

variable "linux_vm_image_publisher" {
  type        = string
  description = "Virtual machine source image publisher"
  default     = "OpenLogic"
}
variable "linux_vm_image_offer" {
  type        = string
  description = "Virtual machine source image offer"
  default     = "CentOS"
}
variable "centos_7_sku" {
  type        = string
  description = "SKU for latest CentOS 8 "
  default     = "7_9"
}
variable "centos_7_gen2_sku" {
  type        = string
  description = "SKU for latest CentOS 8 Gen2"
  default     = "7_9-gen2"
}
variable "centos_8_sku" {
  type        = string
  description = "SKU for latest CentOS 8 "
  default     = "8_5"
}
variable "centos_8_gen2_sku" {
  type        = string
  description = "SKU for latest CentOS 8 Gen2"
  default     = "8_5-gen2"
}

# Azure auth

/* variable "azure_subscription_id" {
  type = string
  description = "Azure Subscription ID"
}
variable "azure_client_id" {
  type = string
  defalut     ="<azure_client_id>"
  description = "Azure Client ID"
}
variable "azure_client_secret" {
  type = string
  description = "Azure Client Secret"
}
variable "azure_tenant_id" {
  type = string
  description = "Azure Tenant ID"
} */
```
```hcl
[root@srv1 ~]# cat output.tf
output "computer_name" {
  value = azurerm_linux_virtual_machine.main.computer_name
}
output "admin_username" {
  value = azurerm_linux_virtual_machine.main.admin_username
}
output "public_ip_address" {
  value = azurerm_linux_virtual_machine.main.public_ip_address
}
```
> Need to Know

### make sure you have ssh key created on local machine

```bash
[root@srv1 ~]# ssh-keygen
```
We have defined `public_key` in `main.tf` file, when linux vm craeted we have to use ssh-key to login 
```hcl
 admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }
```

```Bash
[root@srv1 azure-vm]# tree
.
├── main.tf
├── output.tf
├── plan.maintf
├── README.md
├── terraform.tfstate
├── terraform.tfstate.backup
└── variables.tf

[root@srv1 azure-vm]# terraform validate
Success! The configuration is valid.
[root@srv1 azure-vm]# terraform fmt
[root@srv1 azure-vm]# terraform init
[root@srv1 azure-vm]# terraform plan -out main.plantf
[root@srv1 azure-vm]#  terraform apply main.tfplan
...
Apply complete! Resources: 8 added, 0 changed, 0 destroyed.

Outputs:

admin_username = "adminuser"
computer_name = "azvmlab-vm"
public_ip_address = "20.205.35.219"
[root@srv1 azure-vm]# terraform output
admin_username = "adminuser"
computer_name = "azvmlab-vm"
public_ip_address = "20.205.35.219"
[root@srv1 ~]# az vm list --resource-group azvmlab-resources --show-details -o table
Name        ResourceGroup      PowerState    PublicIps      Fqdns    Location    Zones
----------  -----------------  ------------  -------------  -------  ----------  -------
azvmlab-vm  azvmlab-resources  VM running    20.205.35.219           eastasia
[root@srv1 azure-vm]# ssh adminuser@20.205.35.219
The authenticity of host '20.205.35.219 (20.205.35.219)' can't be established.
ECDSA key fingerprint is SHA256:6DA/ljluFG5cYpgxuDrutNGDsA7SwPPyRzZ2S1ewrpY.
ECDSA key fingerprint is MD5:46:67:ff:6c:87:53:30:d1:ae:67:a3:39:5f:00:bf:3b.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '20.205.35.219' (ECDSA) to the list of known hosts.

Thank you for choosing this Microsoft sponsored CentOS image from OpenLogic!
_______                    ______               _____
__  __ \______________________  / _____________ ___(_)______
_  / / /__  __ \  _ \_  __ \_  /  _  __ \_  __ `/_  /_  ___/
/ /_/ /__  /_/ /  __/  / / /  /___/ /_/ /  /_/ /_  / / /__
\____/ _  .___/\___//_/ /_//_____/\____/_\__, / /_/  \___/
       /_/                              /____/  by Perforce
                           ____           _    ___  ____    _____ ___
                          / ___|___ _ __ | |_ / _ \/ ___|  |___  / _ \
                         | |   / _ \ '_ \| __| | | \___ \     / / (_) |
                         | |__|  __/ | | | |_| |_| |___) |   / / \__, |
                          \____\___|_| |_|\__|\___/|____/   /_(_)  /_/
                                                              (2009)

While OpenLogic support is not including with this image, OpenLogic does
offer Silver (12x5) & Gold (24x7) support options and consulting for
enterprise and/or mission critical systems as well as over 400 open-source
packages.  If interested, email info@perforce.com or call +1 612.517.2100.

[adminuser@azvmlab-vm ~]$ hostnamectl
   Static hostname: azvmlab-vm
         Icon name: computer-vm
           Chassis: vm
        Machine ID: ee6f639ed7044de08fbcaa46cf045b35
           Boot ID: 2dce38ac9edd44db9107e451b054a7a6
    Virtualization: microsoft
  Operating System: CentOS Linux 7 (Core)
       CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-1160.76.1.el7.x86_64
      Architecture: x86-64

```

## clean up 
```
[root@srv1 azure-vm]#  terraform plan -destroy -out main.destroy.tfplan
[root@srv1 azure-vm]#  terraform apply main.destroy.tfplan
...
Apply complete! Resources: 0 added, 0 changed, 8 destroyed.

```
