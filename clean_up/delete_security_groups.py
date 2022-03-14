import boto3
from botocore.exceptions import ClientError
import time


ec2_client = boto3.client('ec2')


def check_sg(sg_name=str):
    try:
        sg_response = ec2_client.describe_security_groups(
            Filters=[
                {
                    'Name': 'group-name',
                    'Values': [ sg_name ]
                },
            ]
        )
    except ClientError as e_ec2:
        print(f'Unexpected error occurred while getting Security Group {sg_name} info:')
        print(e_ec2)
        return None
    return sg_response


def del_sg(sg_name_list=str):
    for each in reversed(sg_name_list):
        sg_response = check_sg(each)
        if not sg_response['SecurityGroups']:
            print(f'Security Group \'{each}\' does not exist')
        else:
            while sg_response['SecurityGroups']:
                try:
                    ec2_client.delete_security_group(
                        GroupName = each
                    )
                except ClientError as e_sg:
                    if e_sg.response['Error']['Code'] == 'DependencyViolation':
                        time.sleep(2)
                        break
                    else:
                        print(f'Unexpected Error occurred while deleting Security Group {each}')
                        print(e_sg)
                        return None
                time.sleep(2)
                sg_response = check_sg(each)
            print(f'Security Group \'{each}\' has been deleted')


if __name__ == '__main__':
    import main
    del_sg(main.sg_name_list)
