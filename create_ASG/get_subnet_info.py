import boto3
from botocore.exceptions import ClientError

sts_client = boto3.client('sts')
ec2_client = boto3.client('ec2')


# to get Subnet info, VPC id is needed
def get_vpc_id():
    try:
        account_id = sts_client.get_caller_identity()['Account']
    except ClientError as e_sts:
        print('Unexpected error during getting Account id')
        print(e_sts)
        return None

    try:
        vpc_info = ec2_client.describe_vpcs(
            Filters=[
                {
                    'Name': 'owner-id',
                    'Values': [account_id]
                }
            ]
        )
    except ClientError as e_vpc:
        print('Unexpected error during getting VPC info')
        print(e_vpc)
        return None

    vpc_id = vpc_info['Vpcs'][0]['VpcId']
    return vpc_id


# check if subnets are already exist before creating new ones
def get_subnets_info():
    vpc_id = get_vpc_id()
    try:
        subnets_info = ec2_client.describe_subnets(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [vpc_id]
                }
            ]
        )
    except ClientError as e_subnet:
        print('Unexpected error during getting subnets info')
        print(e_subnet)
        return None

    # to create a Load Balancer at least 2 AZs needed to use
    # check how many unique AZs set
    availability_zone_set = set()
    for each in subnets_info['Subnets']:
        # collect unique AZs
        availability_zone_set.add(
            each['AvailabilityZone']
        )

    # if AZ's quantity is ok:
    if len(availability_zone_set) >= 2:
        # create SubnetInfo list of dict's:
        # [ {}, {} ... {} ]
        subnets_info_list = []
        for each in subnets_info['Subnets']:
            subnets_info_list.append(
                {
                    'SubnetId': each['SubnetId'],
                    'AvailabilityZone': each['AvailabilityZone'],
                    'CidrBlock': each['CidrBlock']
                }
            )
        return subnets_info_list
    else:
        return 'You should use at least 2 AZs'


if __name__ == "__main__":
    get_subnets_info()
