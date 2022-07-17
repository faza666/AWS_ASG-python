import boto3
from botocore.errorfactory import ClientError

elb_client = boto3.client('elbv2')


def del_lst(alb_name: str):
    try:
        elb = elb_client.describe_load_balancers(
            Names=[alb_name]
        )
    except ClientError as e_elb:
        if e_elb.response['Error']['Code'] == 'LoadBalancerNotFound':
            print(f'A Load Balancer for this Listener does not exist')
            return None
        else:
            print(e_elb)
            return None

    elb_arn = elb['LoadBalancers'][0]['LoadBalancerArn']
    try:
        listener = elb_client.describe_listeners(
            LoadBalancerArn=elb_arn
        )
    except ClientError as e_lis:
        print('Unexpected error occurred while getting the listener info')
        print(e_lis)
        return None

    if listener['Listeners']:
        lst_arn = listener['Listeners'][0]['ListenerArn']
        try:
            elb_client.delete_listener(
                ListenerArn=lst_arn
            )
            print(f'Listener for \'{alb_name}\' has been deleted')
        except ClientError as e:
            print('Unexpected error occurred while deleting the Listener')
            print(e)
    else:
        print('This Listener does not exist')


if __name__ == '__main__':
    import main
    del_lst(main.load_balancer_name)
