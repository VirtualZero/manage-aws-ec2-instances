import boto3
import argparse
import json
from halo import Halo
import os
from termcolor import colored
import datetime


ec2 = boto3.client(
    'ec2',
    region_name='us-east-2',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

script_directory = os.path.dirname(
    os.path.abspath(__file__)
)


def write_to_monitoring_log(response, status_message):
    with open('monitoring.log', 'r+') as monitoring_log:
        log_entry_time = datetime.datetime.now().strftime(
            '%A, %D %I:%M %p'
        )

        monitoring_meta_data = json.dumps(
            response,
            indent=4,
            sort_keys=True,
            default=str
        )

        log_entry = f'{log_entry_time}\n'\
            f'{monitoring_meta_data}\n'

        log_content = monitoring_log.read()
        monitoring_log.seek(0, 0)
        updated_log_content = log_entry.rstrip("\r\n") +\
            '\n\n\n' + log_content

        monitoring_log.write(
            updated_log_content
        )

        print(status_message)

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

            if not os.path.isfile(f'{script_directory}/monitoring.log'):
                open('monitoring.log', 'a').close()
            
            spinner.stop()

            write_to_monitoring_log(response, status_message)

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

        spinner.stop()

    if "'disabling'" in str(response) or\
       "'disabled'" in str(response):
        unicode_chars = '\n\u2714 '
        status_message = f'{colored(unicode_chars, "green")}'\
            f'Detailed monitoring of AWS EC2 instance '\
            f'{instance_id} is disabled. Meta data about every '\
            f'monitoring event is located in '\
            f'{script_directory}/monitoring.log\n'
        
        if not os.path.isfile(f'{script_directory}/monitoring.log'):
            open('monitoring.log', 'a').close()

        spinner.stop()

        write_to_monitoring_log(response, status_message)

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
        help='Retrieves and displays information about your AWS EC2 instances.',
        action='store_true'
    )

    parser.add_argument(
        '-m',
        '--monitor',
        help='Enables detailed monitoring of an AWS EC2 instance.',
        action='store_true'
    )

    parser.add_argument(
        '-u',
        '--unmonitor',
        help='Disables detailed monitoring of an AWS EC2 instance.',
        action='store_true'
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_cli_arguments()

    if args.info:
        get_ec2_info()

    if args.monitor:
        enable_monitoring()

    if args.unmonitor:
        disable_monitoring()


if __name__ == '__main__':
    main()
