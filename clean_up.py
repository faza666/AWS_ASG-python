import clean_up.delete_launch_template as clean_lt
import clean_up.delete_security_groups as clean_sg
import clean_up.delete_load_balancer as clean_lb
import clean_up.delete_target_group as clean_tg
import clean_up.delete_listener as clean_lst
import clean_up.delete_auto_scaling_group as clean_asg
import main


if __name__ == '__main__':
    clean_asg.del_asg(main.auto_scaling_group_name)
    clean_lst.del_lst(main.load_balancer_name)
    clean_lb.del_alb(main.load_balancer_name)
    clean_tg.del_tg(main.target_group_name)
    clean_lt.delete_ec2_launch_template(main.launch_template_name)
    clean_sg.del_sg(main.sg_name_list)
