# deploy-on-aws
in short, we are deploying a web app on aws. there are few ways to deploy our infra and web app on it, so follow the rest of the guide to learn how and what.

tldr - we want to deploy a web app that simply monitor the host its on. for our example, we will assume that it is a linux host, and we are writing the backend of the web app with flask cause I love python.
this app will seat on a comfortable infra on aws, using ec2 and setting up the needed secure network, so we can access that web app from our pc.

as for usage, choose the tool you want to deploy your infra with, and follow the guide bellow.

## the web app
### things to monitor in our linux host
1. general
2. cpu
3. memory
4. disk
5. network
6. security
    - se linux
    - ip tables
    
### deploy locally on docker container
if you want to deploy the web app locally so you can test it easily without the need to deploy the whole aws infra, use docker:
1. install docker $ docker-compose
2. docker compose up -d (in the same folder that your docker-compose.yml is in)

## the aws infra 
we are using the "us-east-1" region because its the cheapest for t3.micro AMI (https://www.instance-pricing.com/provider=aws-ec2/cheapest/).

chef Sean's recipe (the components we will deploy):
 - 1 vpc
 - 1 internet gateway (aws static website public ip)
 - 1 route table
 - 1 subnet (associated with the route table)
 - 1 security group
 - 1 ec2 instance
 - 1 web app (on the ec2 instance)
 
### deploying the infrastructure on aws with Boto3 (python SDK for aws)
1. install python3
2. python3 python-infra/main.py

### deploying the infrastructure on aws with Terraform
1. install aws cli
2. aws configure to set your credentials
2. install terraform
3. terraform init
4. terraform plan
5. terraform apply
 
### deploying the infrastructure on aws with Pulumi
note that the deployment with pulumi in this repo is still in progress.

1. install pulumi
2. install python
3. install awscli if you want to configure your aws login credentials.
    - aws configure
4. pulumi login
5. pulumi preview
6. pulumi up on the same folder where your pulumi's yamls are


# To Do
## tools to add
1. web app monitor with zabbix
2. web app testing with selenium
3. infra deployment with pulumi
4. infra deployment with ansible
## other
1. admin dashboard template https://github.com/jonalxh/Flask-Admin-Dashboard