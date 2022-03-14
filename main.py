import create_ASG.get_subnet_info as subnet
import create_ASG.create_security_groups as security_group
import create_ASG.get_userdata_ready as userdata
import create_ASG.create_launch_template as lt
import create_ASG.create_load_balancer as alb
import create_ASG.create_auto_scaling_group as asg
import create_ASG.create_target_group as tg
import create_ASG.create_listener as lis
import create_ASG.asg_scaling_policy as asg_sp

sg_name_list = [
    'ASG_SG_for_ALB',
    'ASG_SG_for_EC2'
]
user_data_file = 'ec2-user-data.txt'
launch_template_name = 'My_EC2_Template_01'
load_balancer_name = 'My-ALB-for-ASG'
target_group_name = 'TG-for-ASG-ALB'
auto_scaling_group_name = 'My-boto3-ASG_01'
availability_zones = [
    'eu-central-1a',
    'eu-central-1b',
    'eu-central-1c'
]
auto_scaling_policy_name = 'My Autoscaling Policy'


def main():
    # Creating security groups for EC2 and ALB
    sg_info_list = security_group.create_SG(sg_name_list)
    alb_security_group_id = sg_info_list[0]['SecurityGroupId']

    # Encoding 'user data' to send it with Launch Template
    user_data_string = userdata.user_data_envelop(user_data_file)

    # Creating a Launch Template for EC2 instances
    lt.create_launch_template(
        launch_template_name, sg_name_list[1], user_data_string
    )

    # Getting subnet id list to create a Load Balancer
    subnet_info_list = subnet.get_subnets_info()
    subnet_id_list = []
    for each in subnet_info_list:
        subnet_id_list.append(each['SubnetId'])

    # Creating the Load Balancer
    load_balancer = alb.create_load_balancer(
        load_balancer_name, subnet_id_list, alb_security_group_id
    )

    # Creating Target Group for the Load Balancer
    load_balancer_arn = load_balancer['LoadBalancers'][0]['LoadBalancerArn']
    vpc_id = subnet.get_vpc_id()
    target_group = tg.create_target_group(target_group_name, vpc_id)

    # Creating a Listener to connect the Load Balancer with the Target Group
    target_group_arn = target_group['TargetGroups'][0]['TargetGroupArn']
    lis.create_listener(load_balancer_arn, target_group_arn, load_balancer_name)

    # Creating an AutoScaling Group
    asg.create_ASG(
        auto_scaling_group_name,
        target_group_arn,
        launch_template_name,
        availability_zones
    )

    # Add Scaling Policy to the AutoScaling Group
    asg_sp.add_scaling_policy(auto_scaling_group_name, auto_scaling_policy_name)

    # Mission complete :)


if __name__ == "__main__":
    main()
