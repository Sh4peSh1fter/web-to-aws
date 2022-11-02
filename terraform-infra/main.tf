provider "aws" {
  region = var.region
//  default_tags = var.default_tag
}

# Network
resource "aws_vpc" "test_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "flask-app-vpc"
    EnvName = var.env_tag
  }
}

resource "aws_internet_gateway" "test_internet_gateway" {
  vpc_id = aws_vpc.test_vpc.id

  tags = {
    Name = "flask-app-igw"
    EnvName = var.env_tag
  }
}

resource "aws_subnet" "test_subnet" {
//  count = 2
//  cidr_block = var.subnet_cidrs[count.index]
  cidr_block = "10.0.1.0/24"
  vpc_id = aws_vpc.test_vpc.id
  map_public_ip_on_launch = true
  availability_zone = "us-east-1a"

  tags = {
//    Name = "flask-app-subnet-${count.index + 1}"
    EnvName = var.env_tag
  }
}

resource "aws_route_table" "test_route_table" {
  vpc_id = aws_vpc.test_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.test_internet_gateway.id
  }

  tags = {
    Name = "flask-app-rt"
    EnvName = var.env_tag
  }
}

resource "aws_route_table_association" "test_route_table_association" {
//  count = 2
  route_table_id = aws_route_table.test_route_table.id
//  subnet_id = aws_subnet.test_subnet.*.id[count.index]
  subnet_id = aws_subnet.test_subnet.id
}

//resource "aws_default_route_table" "test_default_route_table" {
//  default_route_table_id = aws_vpc.test_vpc.default_route_table_id
//
//  tags = {
//    Name = "flask-app-default-rt"
//    EnvName = var.env_tag
//  }
//}

resource "aws_security_group" "test_sg" {
  name = "test_sg"
  description = "access to public instances"
  vpc_id = aws_vpc.test_vpc.id

  ingress {
    description = "https for my ip address"
    from_port = 443
    protocol = "tcp"
    to_port = 443
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "http for my ip address"
    from_port = 80
    protocol = "tcp"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "ssh for my ip address"
    from_port = 22
    protocol = "tcp"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    protocol = "-1"
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_network_interface" "test_web_server_nic" {
//  count = 2
//  subnet_id = aws_subnet.test_subnet.*.id[count.index]
  subnet_id = aws_subnet.test_subnet.id
  private_ips = ["10.0.1.50"]
  security_groups = [aws_security_group.test_sg.id]
}

resource "aws_eip" "test_eip" {
//  count = 2
  vpc = true
//  network_interface = aws_network_interface.test_web_server_nic[count.index].id
  network_interface = aws_network_interface.test_web_server_nic.id
  associate_with_private_ip = "10.0.1.50"
  depends_on = [aws_internet_gateway.test_internet_gateway]
}

resource "aws_instance" "test_web_server" {
  ami = "ami-08c40ec9ead489470"
  instance_type = "t3.micro"
  availability_zone = "us-east-1a"

  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.test_web_server_nic.id
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y git python3 python3-pip nginx
              git clone https://github.com/Sh4peSh1fter/web-to-aws.git
              export FLASK_APP_PORT=5000
              sudo pip3 install -r /web-to-aws/requirements.txt

              sudo systemctl start nginx
              sudo systemctl enable nginx

              cp -r /web-to-aws/flask-app/nginx-default-conf.txt /etc/nginx/sites-enables/default
              sudo systemctl restart nginx

              sudo chmod +x /web-to-aws/entrypoint.sh
              cd /web-to-aws/flask-app/
              ./entrypoint.sh
              EOF

  tags = {
    Name = "flask-app-web-server-instance"
    EnvName = var.env_tag
  }
}

//data "http" "get_request_to_flask_app" {
//  url = aws_internet_gateway.test_internet_gateway
//
//  # Optional request headers
//  request_headers = {
//    Accept = "application/json"
//  }
//}