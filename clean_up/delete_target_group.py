import boto3
from botocore.errorfactory import ClientError

elb_client = boto3.client('elbv2')


def del_tg(tg_name: str):
    try:
        tg = elb_client.describe_target_groups(
            Names=[tg_name]
        )
    except ClientError as e_tg:
        if e_tg.response['Error']['Code'] == 'TargetGroupNotFound':
            print(f'Target Group \'{tg_name}\' does not exist')
            return None
        else:
            print('unexpected error')
            print(e_tg)
            return None

    tg_arn = tg['TargetGroups'][0]['TargetGroupArn']
    try:
        elb_client.delete_target_group(
            TargetGroupArn=tg_arn
        )
        print(f'Target Group \'{tg_name}\' has been deleted')
    except ClientError as e:
        print('unexpected error')
        print(e)
        return None


if __name__ == '__main__':
    import main
    del_tg(main.target_group_name)
