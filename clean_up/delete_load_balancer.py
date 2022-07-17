import boto3
import time
from botocore.errorfactory import ClientError

elb_client = boto3.client('elbv2')


def del_alb(alb_name: str):
    try:
        elb = elb_client.describe_load_balancers(
            Names=[alb_name]
        )
        elb_arn = elb['LoadBalancers'][0]['LoadBalancerArn']
        elb_client.delete_load_balancer(
            LoadBalancerArn=elb_arn
        )
        try:
            while elb['LoadBalancers']:
                time.sleep(2)
                elb = elb_client.describe_load_balancers(
                    Names=[alb_name]
                )
        except ClientError as e_elb:
            if e_elb.response['Error']['Code'] == 'LoadBalancerNotFound':
                print(f'Load Balancer \'{alb_name}\' has been deleted')
            else:
                print('Unexpected error during ELB deletion:')
                print(e_elb)

    except ClientError as e_elb:
        if e_elb.response['Error']['Code'] == 'LoadBalancerNotFound':
            print(f'Load Balancer \'{alb_name}\' does not exist')
        else:
            print('Unexpected error during ELB deletion:')
            print(e_elb)


if __name__ == '__main__':
    import main

    del_alb(main.load_balancer_name)
