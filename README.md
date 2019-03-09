# Manage AWS EC2 Instances
Powered by [VirtualZero](https://virtualzero.net)

Manage AWS EC2 Instances is a Python script that provides the ability to manage AWS EC2 instances from any Linux terminal. The script provides the following functionality:

  - Retrieve information about EC2 instances
  - Enable/Disable detailed monitoring of EC2 instances
  - Start/Stop EC2 instances
  - Reboot instances
  - Logging

#### Installation
Clone the repository:
```bash
git clone https://github.com/VirtualZero/manage-aws-ec2-instances.git
```

#### Environment

Install Miniconda
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

```bash
chmod +x Miniconda3-latest-Linux-x86_64.sh
```

```bash
./Miniconda3-latest-Linux-x86_64.sh
```

Create Environment
```bash
conda create --name 'manage-aws-ec2-instances' python=3.7
```

Activate Environment
```bash
source activate manage-aws-ec2-instances
```

Install Dependencies
```bash
cd manage-aws-ec2-instances && pip install -r requirements.txt
```

#### Ececution
Manage AWS EC2 Instances can be executed with or without arguments. When executed without arguments, tasks are chosen from a prompt and the script will loop until 'Quit' is chosen from the menu or CTRL + C is entered. When the script is executed with arguments, the task specified with the argument will be performed and the script will exit. Availabe command line arguments are:

  - -i, --info | Retrieves information about EC2 Instances
  - -m, --monitor | Enables detailed monitoring of EC2 instances
  - -u, --unmonitor | Disables detailed monitoring of EC2 instances
  - -s, --start | Starts an EC2 instance
  - -S, --stop | Stops an EC2 instance
  - -r, --reboot | Reboots an EC2 instance

To view the available command line arguments from the terminal, execute the script with the -h or --help argument.

Example usage:
```sh
$ python3 run.py -m
```

#### Logging
Information and metadata about tasks are recorded in logs. The logs will be created as they are needed in the script's directory. The four logs are:

  - monitoring.log - Contains metadata about monitor/unmonitor events
  - instance_state.log - Contains metadata about start/stop events
  - error.log - Contains information about EC2 errors
  - ec2_info.json - Contains detailed EC2 instance information

#### AWS Credentials
The script requires valid AWS access and secret access keys. Although the keys can be added to the settings.py file included with the script, it is always best practice to use environment variables to store sensitive information.