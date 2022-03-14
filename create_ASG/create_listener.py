import boto3
from botocore.errorfactory import ClientError


elb_client = boto3.client('elbv2')


def create_listener(elb_arn=str, tg_arn=str, elb_name=str):
    try:
        listener = elb_client.describe_listeners(
            LoadBalancerArn = elb_arn
        )
    except ClientError as e_lis:
        print('unexpected Error occurred getting listener info')
        print(e_lis)

    if listener['Listeners']:
        print('This Listener already exists')
        return listener
    else:
        try:
            # create listener
            listener = elb_client.create_listener(
                LoadBalancerArn=elb_arn,
                DefaultActions=[
                    {
                        'TargetGroupArn': tg_arn,
                        'Type': 'forward'
                    }
                ],
                Port=80,
                Protocol='HTTP'
            )
            print(f'Listener for \'{elb_name}\' has been created')
            return listener

        except ClientError as e:
            print('Unexpected error during Listener creation:')
            print(e)
            return None





if __name__ == '__main__':
    import main
    # Creating Listener
        # getting ELB ARN
    load_balancer = elb_client.describe_load_balancers(
        Names=[ main.load_balancer_name ]
    )
    load_balancer_arn = load_balancer['LoadBalancers'][0]['LoadBalancerArn']

        # getting Target-Group ARN
    target_group = elb_client.describe_target_groups(
        Names=[ main.target_group_name ]
    )
    target_group_arn = target_group['TargetGroups'][0]['TargetGroupArn']

        # Creating The Listener
    create_listener(load_balancer_arn, target_group_arn, main.load_balancer_name)
