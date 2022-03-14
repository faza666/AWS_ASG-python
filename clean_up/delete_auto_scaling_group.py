import boto3
import time
from botocore.exceptions import ClientError

asg_client = boto3.client('autoscaling')


def del_asg(asg_name):
    try:
        auto_scaling_group = asg_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )
    except ClientError as e_asg:
        print('Unexpected Error occurred while getting AutoScaling Group info:')
        print(e_asg)
        return None

    if auto_scaling_group['AutoScalingGroups']:
        try:
            asg_client.delete_auto_scaling_group(
                AutoScalingGroupName=asg_name,
                ForceDelete=True
            )
        except ClientError as e_asg:
            print('Unexpected Error occurred while creating AutoScaling Group:')
            print(e_asg)
            return None

        print(f'Please wait a few minutes while ASG is deleting')
        while auto_scaling_group['AutoScalingGroups']:
            time.sleep(30)
            print('Still working, please be patient...')
            auto_scaling_group = asg_client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[asg_name]
            )
        print(f'AutoScalingGroup \'{asg_name}\' has been deleted')
    else:
        print(f'Auto-Scaling Group \'{asg_name}\' does not exist')


if __name__ == '__main__':
    import main

    del_asg(main.auto_scaling_group_name)
