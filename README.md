# AWS_ASG-python
This project creates an AutoScaling Group in Amazon Cloud (AWS)
You need to configure connection with AWS in order to run this code

For more information visit the page below:
* https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration

Also you will need to create virtual environement typing in the terminal:
* $ pyton3 -m venv venv
  
Activate virtual environement with line:
* $ source venv/bin/activate    (for Linux)
* $ venv\Scripts\activate.bat   (for Windows)
  
Install needed packeges within virtual environement:
* $ pip install -r requirements.txt

Run "**main.py**" file, it will:
  - create **Security Groups**:
    - for EC2 instance
    - for Elastic Load Balancer
  - create **Launch Template** for EC2 instances using Security Group created before
  - create **Application Load Balanser** (ALB) using Security Group created before
  - create **Target-Group** for ALB
  - create a **Listener** to connect ALB & Target-Group
  - create and launch the **AutoScaling Group** itself
  - add a Target-Tracking **AutoScaling Policy**

Also, you may delete all created features just running "**clean_up.py**" file
