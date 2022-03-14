import boto3
from botocore.exceptions import ClientError

ec2_client = boto3.client('ec2')


def create_security_group(group_name=str):
    security_group = ec2_client.create_security_group(
        GroupName=group_name,
        Description='Security Group for my ASG'
    )
    return security_group['GroupId']


def add_inbound_rules_to_ALB_SG(SG_name=str):
    in_ALB_SG_rule = ec2_client.authorize_security_group_ingress(
        GroupName=SG_name,
        IpPermissions=[
            {
                'FromPort': 80,
                'ToPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'HTTP access from everywhere',
                    }
                ]
            }
        ]
    )
    return in_ALB_SG_rule


def add_inbound_rules_to_EC2_SG(SG_name=str):
    in_HTTP_rule = ec2_client.authorize_security_group_ingress(
        GroupName=SG_name,
        IpPermissions=[
            {
                'FromPort': 80,
                'ToPort': 80,
                'IpProtocol': 'tcp',
                'UserIdGroupPairs': [
                    {
                        'Description': 'HTTP access from ALB',
                        'GroupName': 'ASG_SG_for_ALB'
                    }
                ]
            }
        ]
    )
    in_SSH_rule = ec2_client.authorize_security_group_ingress(
        GroupName=SG_name,
        IpPermissions=[
            {
                'FromPort': 22,
                'ToPort': 22,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'SSH access from everywhere',
                    }
                ]
            }
        ]
    )
    return [in_HTTP_rule, in_SSH_rule]


def create_SG(sg_name_list):
    asg_sg_list = []
    for each in sg_name_list:
        group_name = each

        try:
            security_group = ec2_client.describe_security_groups(
                GroupNames=[group_name]
            )
            print(f'The Security Group \'{group_name}\' already exists')
            sg_id = security_group['SecurityGroups'][0]['GroupId']
        except ClientError as e_ec2:
            if e_ec2.response['Error']['Code'] == 'InvalidGroup.NotFound':
                try:
                    sg_id = create_security_group(group_name)
                    print(f'The Security Group \'{group_name}\' has been created')
                    if each == sg_name_list[0]:
                        add_inbound_rules_to_ALB_SG(group_name)
                    elif each == sg_name_list[1]:
                        add_inbound_rules_to_EC2_SG(group_name)
                    print(f'Inbound rules for Security Group \'{group_name}\' has been added')
                except ClientError as e_sg:
                    sg_id = None
                    print('Unexpected ERROR')
                    print(e_sg)
            else:
                sg_id = None
                print('unexpected error')

        asg_sg_list.append(
            {
                'SecurityGroupName': group_name,
                'SecurityGroupId': sg_id
            }
        )

    return asg_sg_list


if __name__ == '__main__':
    import main

    print(create_SG(main.sg_name_list))
