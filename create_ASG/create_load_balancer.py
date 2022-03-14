import boto3
import create_ASG.get_subnet_info as vpc
from botocore.errorfactory import ClientError


elb_client = boto3.client('elbv2')
ec2_client = boto3.client('ec2')


def create_load_balancer(
        load_balancer_name=str,
        subnet_id_list=list,
        alb_sg_id=str
):
    try:
        # Check if Load Balancer already exists
        load_balancer = elb_client.describe_load_balancers(
            Names=[ load_balancer_name ]
        )
        if load_balancer:
            print(f'Load Balancer \'{load_balancer_name}\' already exists')
            return load_balancer

    except ClientError as e_elb:
        if e_elb.response['Error']['Code'] == 'LoadBalancerNotFound':

            try:
                # Creating Load Balancer
                load_balancer = elb_client.create_load_balancer(
                    Name = load_balancer_name,
                    Subnets = subnet_id_list,
                    SecurityGroups=[alb_sg_id],
                    Scheme='internet-facing',
                    Tags=[
                        {
                            'Key': 'Purpose',
                            'Value': 'For my ASG'
                        }
                    ],
                    Type='application',
                    IpAddressType='ipv4'
                )
                print(f'Load Balancer \'{load_balancer_name}\' has been created')
                return load_balancer
            except ClientError as e:
                print('Unexpected error during ELB creation:')
                print(e)
                return None

        else:
            print('Unexpected error during ELB creation:')
            print(e_elb)
            return None



if __name__ == '__main__':
    import main
    elb_security_group = ec2_client.describe_security_groups(
        GroupNames = [ main.sg_name_list[0] ]
    )

    # getting subnet id list
    subnet_info_list = vpc.get_subnets_info()
    subnet_id_list = []
    for each in subnet_info_list:
        subnet_id_list.append(each['SubnetId'])

    load_balancer_sg_id = elb_security_group['SecurityGroups'][0]['GroupId']
    create_load_balancer(main.load_balancer_name, subnet_id_list, load_balancer_sg_id)