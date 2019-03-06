import boto3
import argparse
import json
from halo import Halo
import os
from termcolor import colored


ec2 = boto3.client(
    'ec2',
    region_name='us-east-2',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', 
        '--info', 
        help='Retrieves and displays information about your AWS EC2 instances.', 
        action='store_true'
    )

    args = parser.parse_args()

    if args.info:
        get_ec2_info()



if __name__ == '__main__':
    main()
