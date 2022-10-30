# deploy-on-aws

we are using the "us-east-1" region because its the cheapest for t3.micro AMI (https://www.instance-pricing.com/provider=aws-ec2/cheapest/).



Chef Sean's recipe (the components we will deploy):
 - 2 vpc
 - 1 internet gateway (aws static website public ip)
 - 1 route table
 - 1 subnet (associated with the route table)
 - 1 security group
 - 1 ec2 instance
 - 1 web app (on the ec2 instance)

# things to monitor in your linux host
1. general
2. cpu
3. memory
4. disk
5. network
6. security
    - se linux
    - ip tables

# To Do
## tools to add
1. web app monitor with zabbix
2. infra deployment with pulumi
## other
1. admin dashboard template https://github.com/jonalxh/Flask-Admin-Dashboard