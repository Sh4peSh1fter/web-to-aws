import boto3


def create_aws_env(ec2):
    # create vpc
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc.create_tags(Tags=[{"Key": "EnvName", "Value": "Test Environment"}])
    vpc.wait_until_available()
    print(vpc.id)

    # create internet gateway
    igw = ec2.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=igw.id)
    print(igw.id)

    # create route table
    rt = vpc.create_route_table()
    route = rt.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=igw.id)
    print(rt.id)

    # create subnet
    subnet = ec2.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc.id)
    rt.associate_with_subnet(SubnetId=subnet.id)
    print(subnet.id)

    # create security group
    sg = ec2.create_security_group(GroupName='test_sg', Description='only allow SSH, HTTP & HTTPS traffic',
                                   VpcId=vpc.id)
    sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
    sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)
    sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=443, ToPort=443)
    print(sg.group_id)

    # create ec2 instance
    instances = ec2.create_instances(
        ImageId='ami-08c40ec9ead489470',
        InstanceType='t3.micro',
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[{
            'SubnetId': subnet.id,
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': [sg.group_id]
        }],
        UserData='''#!/bin/bash
            sudo apt-get update -y
            sudo apt-get install -y git python3 python3-pip nginx
            git clone https://github.com/Sh4peSh1fter/web-to-aws.git
            export FLASK_APP_PORT=5000
            sudo pip3 install -r /web-to-aws/flask-app/requirements.txt
            
            sudo systemctl start nginx
            sudo systemctl enable nginx
            
            cp -r /web-to-aws/flask-app/nginx-default-conf.txt /etc/nginx/sites-enables/default
            sudo systemctl restart nginx
            
            sudo chmod +x /web-to-aws/flask-app/entrypoint.sh
            cd /web-to-aws/flask-app/
            ./entrypoint.sh
        ''')
    instances[0].wait_until_running()
    print(instances[0].public_ip_address)


def delete_aws_env():
    pass


def main():
    op = input("create / delete\n> ")

    ec2 = boto3.resource('ec2', aws_access_key_id='',
                         aws_secret_access_key='', region_name='us-east-1')

    if op == "create":
        create_aws_env(ec2)
    elif op == "delete":
        delete_aws_env()
    else:
        pass


if __name__ == '__main__':
    main()
