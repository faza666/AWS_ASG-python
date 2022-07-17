import boto3
from botocore.exceptions import ClientError

ec2_client = boto3.client('ec2')


def delete_ec2_launch_template(launch_template_name: str):
    try:
        ec2_client.delete_launch_template(
            LaunchTemplateName=launch_template_name
        )
        print(f'Launch Template \'{launch_template_name}\' has been deleted')
    except ClientError as e_lt:
        if e_lt.response['Error']['Code'] == \
                'InvalidLaunchTemplateName.NotFoundException':
            print(f'Launch Template \'{launch_template_name}\' does not exist')
        else:
            print('unexpected error')


if __name__ == '__main__':
    import main

    delete_ec2_launch_template(main.launch_template_name)
