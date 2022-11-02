output "ec2_public_ip" {
  value = aws_instance.test_web_server.public_ip
}

//output "get_request_to_flask_app_output" {
//  value = data.get_request_to_flask_app
//}
