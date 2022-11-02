"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws


vpc = pulumi_aws.ec2.Vpc(
            "test_vpc",
            cidr_block="10.0.0.0/16",
            )

subnet = pulumi_aws.ec2.Subnet(
    "test_subnet",
    vpc_id=vpc.id,
    availability_zone="us-east-1a",
    cidr_block="10.0.0.0/16",
)

sg = pulumi_aws.ec2.SecurityGroup(
    "sg",
    description="",
    ingress = [
        {
            "protocol": "tcp",
            "from_port": 443,
            "to_port": 443,
            "cidr_blocks": ["0.0.0.0/0"]
        }
    ],
    ingress = [
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"]
        }
    ],
    ingress = [
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"]
        }
    ],
    egress = [
        {
            "protocol": "-1",
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"]
        }
    ],
)

ami = pulumi_aws.ec2.get_ami()

instance = pulumi_aws.ec2.Instance(
    "flask-app",
    instance_type="t3.micro",
    vpc_security_group_ids=[sg.id],
    subnet_id=subnet.id,
    ami=ami.id
)

# Export the name of the bucket
pulumi.export('ec2 id', instance.id)
pulumi.export('vpc id', vpc.id)
