import boto3
from botocore.errorfactory import ClientError
import create_ASG.get_subnet_info as vpc

elb_client = boto3.client('elbv2')


def create_target_group(tg_name=str, vpc_id=str):
    try:
        target_group = elb_client.describe_target_groups(
            Names=[ tg_name ]
        )
        print(f'Target-Group \'{tg_name}\' already exists')
        return target_group
    except ClientError as e_tg:
        if e_tg.response['Error']['Code'] == 'TargetGroupNotFound':
            try:
                target_group = elb_client.create_target_group(
                    Name=tg_name,
                    Protocol='HTTP',
                    ProtocolVersion='HTTP1',
                    Port=80,
                    VpcId=vpc_id,
                    HealthCheckProtocol='HTTP',
                    HealthCheckPort='traffic-port',
                    HealthCheckEnabled=True,
                    HealthCheckPath='/index.html',
                    HealthCheckIntervalSeconds=30,
                    HealthCheckTimeoutSeconds=5,
                    HealthyThresholdCount=2,
                    UnhealthyThresholdCount=2,
                    Matcher={
                        'HttpCode': '200'
                    },
                    TargetType='instance',
                    Tags=[
                        {
                            'Key': 'Purpose',
                            'Value': 'TG for ASG ALB'
                        }
                    ]
                )
                print(f'Target Group \'{tg_name}\' has been created')
                return target_group

            except ClientError as e:
                print('Unexpected Error occurred during Target-Group creation')
                print(e)
                return None
        else:
            print('Unexpected Error occurred during getting Target-Group info')
            print(e_tg)
            return None


if __name__ == '__main__':
    import main
    vpc_id = vpc.get_vpc_id()
    create_target_group(main.target_group_name, vpc_id)
