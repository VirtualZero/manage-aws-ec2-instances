import boto3
import argparse
import json
from halo import Halo
import os
from termcolor import colored
import datetime
from botocore.exceptions import ClientError
from settings import get_settings
import re


settings = get_settings()

ec2 = boto3.client(
    'ec2',
    region_name=settings['aws_ec2_region_name'],
    aws_access_key_id=settings['aws_access_key_id'],
    aws_secret_access_key=settings['aws_secret_access_key']
)

script_directory = os.path.dirname(
    os.path.abspath(__file__)
)


def handle_ec2_errors(e, flags):
    error = str(e)

    unicode_chars = '\n\u2718 '
    print(
        f'{colored(unicode_chars, "red")}'
        f'{error}\n'
    )

    write_to_log(
        'error',
        error,
        ''    
    )

    if flags:
        exit(1)

    return 'ec2_error'


def reboot_instance(instance_id):
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

            return True

        except ClientError as e:
            spinner.stop()
            handle_ec2_errors(e)
        

def stop_instance(instance_id):
    with Halo(
        text='Stopping Instance...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:

        try:
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

                spinner.stop()
                write_to_log(
                    'instance_state',
                    response,
                    status_message
                )

                return True

            else:
                unicode_chars = '\n\u2718 '
                print(
                    f'{unicode_chars} Something went wrong, try again.'
                )

                return False

        except ClientError as e:
            spinner.stop()
            handle_ec2_errors(e)


def write_to_log(log_name, response, status_message):
    check_for_log(log_name)
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

        if status_message:
            print(status_message)

        return True


def start_instance(instance_id, flags):
    with Halo(
        text='Starting Instance...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:

        try:
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

                spinner.stop()
                write_to_log(
                    'instance_state',
                    response, 
                    status_message
                )

                return True

            else:
                unicode_chars = '\n\u2718 '
                print(
                    f'{unicode_chars} Something went wrong, try again.'
                )

                return False

        except ClientError as e:
            spinner.stop()
            return handle_ec2_errors(e, flags)


def check_for_log(log_name):
    if not os.path.isfile(f'{script_directory}/{log_name}.log'):
        open(f'{log_name}.log', 'a').close()

    return True


def enable_monitoring(instance_id, flags):
    with Halo(
        text='Enabling Detailed Instance Monitoring...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:

        try:
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

                spinner.stop()
                write_to_log(
                    'monitoring', 
                    response, 
                    status_message
                )

                return True

            else:
                unicode_chars = '\n\u2718 '
                print(
                    f'{unicode_chars} Something went wrong, try again.'
                )

                return False

        except ClientError as e:
            spinner.stop()
            return handle_ec2_errors(e, flags)


def disable_monitoring(instance_id, flags):
    with Halo(
        text='Disabling Detailed Instance Monitoring...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:

        try:
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

                return False

            return True

        except ClientError as e:
            spinner.stop()
            return handle_ec2_errors(e, flags)


def get_ec2_info(flags):
    with Halo(
        text='Requesting EC2 Information...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:

        with open('ec2_info.json', 'w') as info_file:
            try:
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

            except ClientError as e:
                spinner.stop()
                return handle_ec2_errors(e, flags)

    print(saved_file_message)

    return True


def parse_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--info',
        help=f'Retrieves and saves information '\
             f'about your AWS EC2 instances',
        action='store_true'
    )

    parser.add_argument(
        '-m',
        '--monitor',
        help=f'Enables detailed monitoring of an AWS '\
             f'EC2 instance',
        action='store_true'
    )

    parser.add_argument(
        '-u',
        '--unmonitor',
        help=f'Disables detailed monitoring of an '
             f'AWS EC2 instance',
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


def get_task():
    task = input(
        f'\nWhat would you like to do:\n'
        f'1) Get EC2 instance information\n'
        f'2) Enable detailed monitoring of an instance\n'
        f'3) Disable detailed monitoring of an instance\n'
        f'4) Start an instance\n'
        f'5) Stop an instance\n'
        f'6) Reboot an instance\n'
        f'7) Quit\n\n'
        f'Your choice: '
    )

    unicode_chars = '\n\u2718 '
    error_message = f'{colored(unicode_chars, "red")}'\
                    f'Invalid Input'

    if task.isdigit():
        if int(task) not in range(1,8):
            print(error_message)
            return False

    else:
        print(error_message)
        return False

    return task


def main():
    try:
        args = parse_cli_arguments()

        if 'True' not in str(args):
            quit = False

            while not quit:
                task = int(get_task())
                flags = False

                if task:
                    if task != 1 and task != 7:
                        instance_id = input('Enter the AWS EC2 instance ID: ')

                    if task == 1:
                        status = get_ec2_info(flags)

                    if task == 2:
                        status = enable_monitoring(instance_id, flags)

                    if task == 3:
                        status = disable_monitoring(instance_id, flags)

                    if task == 4:
                        status = start_instance(instance_id, flags)

                    if task == 5:
                        status = status = stop_instance(instance_id)

                    if task == 6:
                        status = reboot_instance(instance_id)

                    if task != 7:
                        if not status:
                            exit(1)

                    if task == 7:
                        quit = True

            print('\nGoodbye\n')
            exit(0)

        flags = True

        if args.info:
            status = get_ec2_info(flags)

        if args.monitor:
            instance_id = input('Enter the AWS EC2 instance ID: ')
            status = enable_monitoring(instance_id, flags)

        if args.unmonitor:
            instance_id = input('Enter the AWS EC2 instance ID: ')
            status = disable_monitoring(instance_id, flags)

        if args.start:
            instance_id = input('Enter the AWS EC2 instance ID: ')
            status = start_instance(instance_id)

        if args.stop:
            instance_id = input('Enter the AWS EC2 instance ID: ')
            status = stop_instance(instance_id)

        if args.reboot:
            instance_id = input('Enter the AWS EC2 instance ID: ')
            status = reboot_instance(instance_id)

        if not status:
            exit(1)

        exit(0)

    except KeyboardInterrupt:
        print('\n\nGoodbye\n')
        exit(0)


if __name__ == '__main__':
    main()
