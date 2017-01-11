EC2_DNS = ec2-35-162-48-28.us-west-2.compute.amazonaws.com
SSH_KEY=~/.ssh/linux-webserv.pem

connect-to-ec2:
	@echo 'Connect to $(EC2_DNS)'
	ssh -i $(SSH_KEY) ubuntu@$(EC2_DNS)
