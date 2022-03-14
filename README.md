# AWS_ASG
This project creates an AutoScaling Group in Amazon Cloud (AWS)
You need to configure connection with AWS in order to run this code

For more information visit the page below:
  https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
  
Just run "main.py" file, it will:
    - create Security Groups:
        for EC2 instance
        for Elastic Load Balancer
    - create Launch Template for EC2 instances
    - create Application Load Balanser
    - create Target-Group for ALB
    - create a Listener to connect ALB & Target-Group
    - create and launch the AutoScaling Group itself
    - add a Target-Tracking AutoScaling Policy
Also, you may close down and delete all created features
  Just run clean_up.py
