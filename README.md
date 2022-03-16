# AWS_ASG-python
This project creates an AutoScaling Group in Amazon Cloud (AWS)
You need to configure connection with AWS in order to run this code

For more information visit the page below:
  https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
Don't forget to set default region along with your credentials.

Also you will need to create virtual environement typing in the terminal:
  $ pyton3 -m venv venv
  
Activate virtual environement with line:
  $ source venv/bin/activate    (for Linux)
  $ venv\Scripts\activate.bat   (for Windows)
  
Install needed packeges within virtual environement:
  $ pip install -r requirements.txt

Don't forget to deactivate venv AFTER you use this script with line:
  $ deactivate                    (for Linux)
  $ venv\Scripts\deactivate.bat   (for Windows)

Just run "main.py" file, it will:
    - create Security Groups:
        for EC2 instance
        for Elastic Load Balancer
    - create Launch Template for EC2 instances
    - create Application Load Balanser (ALB)
    - create Target-Group for ALB
    - create a Listener to connect ALB & Target-Group
    - create and launch the AutoScaling Group itself
    - add a Target-Tracking AutoScaling Policy
Also, you may close down and delete all created features
  Just run clean_up.py
