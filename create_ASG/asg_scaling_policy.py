import boto3
from botocore.errorfactory import ClientError

asg_client = boto3.client('autoscaling')


def add_scaling_policy(asg_name=str, scaling_policy_name=str):
    try:
        scaling_policy = asg_client.describe_policies(
            AutoScalingGroupName=asg_name,
            PolicyNames=[scaling_policy_name]
        )
    except ClientError as e_scp:
        print('Unexpected Error occurred while getting Scaling Policy info:')
        print(e_scp)
        return None
    if scaling_policy['ScalingPolicies']:
        print(f'Scaling Policy \'{scaling_policy_name}\' already exists')
        return scaling_policy
    else:
        try:
            scaling_policy = asg_client.put_scaling_policy(
                AutoScalingGroupName=asg_name,
                PolicyName=scaling_policy_name,
                PolicyType='TargetTrackingScaling',
                EstimatedInstanceWarmup=30,
                TargetTrackingConfiguration={
                    'PredefinedMetricSpecification': {
                        'PredefinedMetricType': 'ASGAverageCPUUtilization'
                    },
                    'TargetValue': 50,
                    'DisableScaleIn': False
                },
                Enabled=True | False
            )
            print(f'Scaling Policy \'{scaling_policy_name}\' successfully added to AutoScaling Group \'{asg_name}\'')
            return scaling_policy
        except ClientError as e_sp:
            print('Unexpected Error occurred while adding Scaling Policy to the AutoScaling Group:')
            print(e_sp)
            return None


if __name__ == '__main__':
    import main

    add_scaling_policy(main.auto_scaling_group_name, main.auto_scaling_policy_name)
