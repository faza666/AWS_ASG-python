import boto3
import create_ASG.get_userdata_ready as user_data
from botocore.exceptions import ClientError

ec2_client = boto3.client('ec2')


def create_launch_template(lt_name: str, ec2_sg_name: str, user_data_string: str):
    try:
        launch_template = ec2_client.create_launch_template(
            LaunchTemplateName=lt_name,
            VersionDescription='Template to create EC2-instances within my ASG',
            LaunchTemplateData={
                'ImageId': 'ami-07df274a488ca9195',
                'InstanceType': 't2.micro',
                'KeyName': 'EC2 Tutorial',
                'UserData': user_data_string,
                'BlockDeviceMappings': [
                    {
                        'DeviceName': '/dev/xvda',
                        'Ebs': {
                            'Encrypted': False,
                            'DeleteOnTermination': True,
                            'VolumeSize': 8,
                            'VolumeType': 'gp2',
                        }
                    }
                ],
                'InstanceInitiatedShutdownBehavior': 'terminate',
                'SecurityGroups': [
                    ec2_sg_name
                ],
                'TagSpecifications': [
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Purpose',
                                'Value': 'For ASG'
                            }
                        ]
                    }
                ]
            },
            TagSpecifications=[
                {
                    'ResourceType': 'launch-template',
                    'Tags': [
                        {
                            'Key': 'purpose',
                            'Value': 'for my ASG'
                        }
                    ]
                }
            ]
        )
        print(f'Launch Template \'{lt_name}\' has been created')
        return launch_template
    except ClientError as e_lt:
        if e_lt.response['Error']['Code'] == 'InvalidLaunchTemplateName.AlreadyExistsException':
            print(f'Launch template \'{lt_name}\' already exists')
            return None
        else:
            print('Unexpected error occurred while creating Launch Template')
            print(e_lt)
            return None


if __name__ == '__main__':
    import main

    user_data = user_data.user_data_envelop('../' + main.user_data_file)
    create_launch_template(
        main.launch_template_name, main.sg_name_list[1], user_data
    )
