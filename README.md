# DevOps cloud infrastructure automatization with CI/CD

## Schemas

![Alt text](common/images/diagram.png?raw=true "Title")

## Description

DevOps cloud infrastructure automatization with CI/CD

### requirements

```yaml
OS: Centos 7+ (yum required)
python: python3
```

## Usage

### git-clone

```bash
git clone https://github.com/gadzillos/DevOps-automation.git
cd repo
```

### command line

Used to start the script from working directory, requieries file written token for Azure Service Principal

```bash
python3 launch.py --path ~/path_to_Azure_token.json
```

### token format (Service Principal)

```json
{
  "appId": "00000000-0000-0000-0000-000000000000",
  "password": "0000-0000-0000-0000-000000000000",
  "tenant": "00000000-0000-0000-0000-000000000000",
  "subscriptionId": "00000000-0000-0000-0000-000000000000"
}
```

## Overview
