# Manage AWS EC2 Instances
Powered by [VirtualZero](https://virtualzero.net)

Manage AWS EC2 Instances is a Python script that provides the ability to manage AWS EC2 instances from any Linux terminal. The script provides the following functionality:

  - Retrieve information about EC2 instances
  - Enable/Disable detailed monitoring of EC2 instances
  - Start/Stop EC2 instances
  - Reboot instances
  - Logging

Manage AWS EC2 Instances can be executed with or without arguments. When executed without arguments, tasks are chosen from a prompt and the script will loop 
until 'Quit' is chosen from the menu or CTRL + C is entered. When the script is executed with arguments, the task specified with the argument 
will be performed and the script will exit. Availabe command line arguments are:

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

##### AWS Credentials
The script requires valid AWS access and secret access keys. Although the keys can be added to the settings.py file included with the script, it is always best practice to use environment variables to store sensitive information.