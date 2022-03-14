import boto3
from botocore.errorfactory import ClientError
import yaml


elb_client = boto3.client('elbv2')
asg_client = boto3.client('autoscaling')


def create_ASG(auto_scaling_group_name=str, target_group_arn=str,
               launch_template_name=str, availability_zones=list):
    try:
        auto_scaling_group = asg_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[auto_scaling_group_name]
        )
    except ClientError as e_asg:
        print('Unexpected Error occurred while getting AutoScaling Group info:')
        print(e_asg)
        return None

    if auto_scaling_group['AutoScalingGroups']:
        print(f'Auto-Scaling Group {auto_scaling_group_name} already exists')
    else:
        try:
            auto_scaling_group = asg_client.create_auto_scaling_group(
                AutoScalingGroupName=auto_scaling_group_name,
                LaunchTemplate={
                    'LaunchTemplateName': launch_template_name,
                },
                MinSize=1,
                MaxSize=3,
                DesiredCapacity=1,
                DefaultCooldown=30,
                AvailabilityZones=availability_zones,
                TargetGroupARNs=[
                    target_group_arn
                ],
                HealthCheckType='ELB',
                HealthCheckGracePeriod=0,
                NewInstancesProtectedFromScaleIn=False,
                CapacityRebalance=False,
                Tags=[
                    {
                        'ResourceId': auto_scaling_group_name,
                        'ResourceType': 'auto-scaling-group',
                        'Key': 'Purpose',
                        'Value': 'Test my ASG',
                        'PropagateAtLaunch': True
                    }
                ]
            )
            print(f'Auto-Scaling Group {auto_scaling_group_name} has been created')
        except ClientError as e_asg:
            print('Unexpected Error occurred while creating AutoScaling Group:')
            print(e_asg)
            return None

    with open('ASG_info.txt', 'w') as asg_info_file:
        asg_info_file.write(yaml.dump(auto_scaling_group))
    return auto_scaling_group


if __name__ == '__main__':
    import main

    # getting Target-Group arn
    tg = elb_client.describe_target_groups(
        Names=[main.target_group_name]
    )
    tg_arn = tg['TargetGroups'][0]['TargetGroupArn']

    # Creating AutoScaling Group
    asg_name = main.auto_scaling_group_name
    lt_name = main.launch_template_name
    AZs = main.availability_zones
    asg = create_ASG(asg_name, tg_arn, lt_name, AZs)
