import boto3
import argparse
import json
from halo import Halo
import os
from termcolor import colored
import datetime
from botocore.exceptions import ClientError


ec2 = boto3.client(
    'ec2',
    region_name='us-east-2',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

script_directory = os.path.dirname(
    os.path.abspath(__file__)
)


def reboot_instance():
    instance_id = input('Enter the AWS EC2 instance ID: ')

    with Halo(
        text='Stopping Instance...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:
        
        try:
            ec2.reboot_instances(
                InstanceIds=[instance_id],
                DryRun=False
            )

            spinner.stop()

            unicode_chars = '\n\u2714 '
            print(
                f'{colored(unicode_chars, "green")}'
                f'AWS EC2 instance {instance_id} '\
                f'is rebooting.\n'
            )

        except ClientError as e:
            spinner.stop()
            if 'IncorrectState' in str(e):
                unicode_chars = '\n\u2718 '
                print(
                    f'{colored(unicode_chars, "red")}'\
                    f'Instance is stopped, cannot reboot.\n'
                )
        

def stop_instance():
    instance_id = input('Enter the AWS EC2 instance ID: ')

    with Halo(
        text='Stopping Instance...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:
        response = ec2.stop_instances(
            InstanceIds=[instance_id],
            DryRun=False
        )

        if "'stopping'" in str(response) or\
           "'stopped'" in str(response):
            unicode_chars = '\n\u2714 '
            status_message = f'{colored(unicode_chars, "green")}'\
                f'AWS EC2 instance {instance_id} is '\
                f'stopped. Meta data about every '\
                f'start/stop event is located in '\
                f'{script_directory}/instance_state.log\n'

            check_for_log('instance_state')
            spinner.stop()
            write_to_log(
                'instance_state',
                response,
                status_message
            )

        else:
            unicode_chars = '\n\u2718 '
            print(
                f'{unicode_chars} Something went wrong, try again.'
            )


def write_to_log(log_name, response, status_message):
    with open(f'{log_name}.log', 'r+') as log:
        log_entry_time = datetime.datetime.now().strftime(
            '%A, %D %I:%M %p'
        )

        meta_data = json.dumps(
            response,
            indent=4,
            sort_keys=True,
            default=str
        )

        log_entry = f'{log_entry_time}\n'\
            f'{meta_data}\n'

        log_content = log.read()
        log.seek(0, 0)
        updated_log_content = log_entry.rstrip("\r\n") +\
            '\n\n\n' + log_content

        log.write(
            updated_log_content
        )

        print(status_message)

        return True


def start_instance():
    instance_id = input('Enter the AWS EC2 instance ID: ')

    with Halo(
        text='Starting Instance...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:
        response = ec2.start_instances(
            InstanceIds=[instance_id], 
            DryRun=False
        )

        if "'pending'" in str(response) or\
           "'running'" in str(response):
            unicode_chars = '\n\u2714 '
            status_message = f'{colored(unicode_chars, "green")}'\
                f'AWS EC2 instance {instance_id} is '\
                f'started. Meta data about every '\
                f'start/stop event is located in '\
                f'{script_directory}/instance_state.log\n'

            check_for_log('instance_state')
            spinner.stop()
            write_to_log(
                'instance_state',
                response, 
                status_message
            )

        else:
            unicode_chars = '\n\u2718 '
            print(
                f'{unicode_chars} Something went wrong, try again.'
            )


def check_for_log(log_name):
    if not os.path.isfile(f'{script_directory}/{log_name}.log'):
        open(f'{log_name}.log', 'a').close()

    return True


def enable_monitoring():
    instance_id = input('Enter the AWS EC2 instance ID: ')

    with Halo(
        text='Enabling Detailed Instance Monitoring...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:
        response = ec2.monitor_instances(
            InstanceIds=[instance_id]
        )

        if "'enabled'" in str(response) or\
           "'pending'" in str(response):
            unicode_chars = '\n\u2714 '
            status_message = f'{colored(unicode_chars, "green")}'\
                f'Detailed monitoring of AWS EC2 instance '\
                f'{instance_id} is enabled. Meta data about every '\
                f'monitoring event is located in '\
                f'{script_directory}/monitoring.log\n'

            check_for_log('monitoring')
            spinner.stop()
            write_to_log(
                'monitoring', 
                response, 
                status_message
            )

        else:
            unicode_chars = '\n\u2718 '
            print(
                f'{unicode_chars} Something went wrong, try again.'
            )


def disable_monitoring():
    instance_id = input('Enter the AWS EC2 instance ID: ')

    with Halo(
        text='Disabling Detailed Instance Monitoring...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:
        response = ec2.unmonitor_instances(
            InstanceIds=[instance_id]
        )

    if "'disabling'" in str(response) or\
       "'disabled'" in str(response):
        unicode_chars = '\n\u2714 '
        status_message = f'{colored(unicode_chars, "green")}'\
            f'Detailed monitoring of AWS EC2 instance '\
            f'{instance_id} is disabled. Meta data about every '\
            f'monitoring event is located in '\
            f'{script_directory}/monitoring.log\n'
        
        check_for_log('monitoring')
        spinner.stop()
        write_to_log(
            'monitoring',
            response, 
            status_message
        )

    else:
        unicode_chars = '\n\u2718 '
        print(
            f'{unicode_chars} Something went wrong, try again.'
        )


def get_ec2_info():
    with Halo(
        text='Requesting EC2 Information...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:

        with open('ec2_info.json', 'w') as info_file:
            info_file.write(
                json.dumps(
                    ec2.describe_instances(),
                    indent=4,
                    sort_keys=True,
                    default=str
                )
            )

            unicode_chars = '\n\u2714 '
            saved_file_message = f'{colored(unicode_chars, "green")}'\
                f'Your AWS EC2 information has been saved in '\
                f'{os.path.dirname(os.path.abspath(__file__))}'\
                f'/ec2_info.json\n'

            spinner.stop()

    print(saved_file_message)

    return True


def parse_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--info',
        help='Retrieves and displays information about your AWS EC2 instances',
        action='store_true'
    )

    parser.add_argument(
        '-m',
        '--monitor',
        help='Enables detailed monitoring of an AWS EC2 instance',
        action='store_true'
    )

    parser.add_argument(
        '-u',
        '--unmonitor',
        help='Disables detailed monitoring of an AWS EC2 instance',
        action='store_true'
    )

    parser.add_argument(
        '-s',
        '--start',
        help='Starts an AWS EC2 instance',
        action='store_true'
    )

    parser.add_argument(
        '-S',
        '--stop',
        help='Stops an AWS EC2 instance',
        action='store_true'
    )

    parser.add_argument(
        '-r',
        '--reboot',
        help='Reboots an AWS EC2 instance',
        action='store_true'
    )

    return parser.parse_args()


def main():
    args = parse_cli_arguments()

    if args.info:
        get_ec2_info()

    if args.monitor:
        enable_monitoring()

    if args.unmonitor:
        disable_monitoring()

    if args.start:
        start_instance()

    if args.stop:
        stop_instance()

    if args.reboot:
        reboot_instance()


if __name__ == '__main__':
    main()
