provider "aws" {
  profile = "default"
  region     = "us-east-1"
}

# Create Security Group
resource "aws_security_group" "sg" {
    name        = "web-elb-sg-cd-3"
    description = "web-elb-sg-cd-3"
    vpc_id      = var.my_vpc_id

    ingress {
        from_port       = 80
        to_port         = 80
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
        ipv6_cidr_blocks     = ["::/0"]
    }

    ingress {
        from_port       = 8000
        to_port         = 8000
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
        ipv6_cidr_blocks     = ["::/0"]
    }

    ingress {
        from_port       = 22
        to_port         = 22
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
        ipv6_cidr_blocks     = ["::/0"]
    }

    ingress {
        from_port       = 443
        to_port         = 443
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
        ipv6_cidr_blocks     = ["::/0"]
    }

    ingress {
        from_port       = 5432
        to_port         = 5432
        protocol        = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
        ipv6_cidr_blocks     = ["::/0"]
    }

    egress {
        from_port       = 0
        to_port         = 0
        protocol        = "-1"
        cidr_blocks     = ["0.0.0.0/0"]
    }
}

# Create Launch Configuration
resource "aws_launch_configuration" "launch_config" {
    name                        = "config-env-3"
    image_id                    = var.my_ami_id
    instance_type               = "t2.micro"
    iam_instance_profile        = "arn:aws:iam::664379268339:instance-profile/AmazonSSMRoleForInstancesQuickSetup"
    key_name                    = "iluovo_key"
    security_groups             = [aws_security_group.sg.id]
    enable_monitoring           = false
    ebs_optimized               = false

    root_block_device {
        volume_type           = "gp2"
        volume_size           = 20
        delete_on_termination = true
    }
}

# Create Auto Scaling Group
resource "aws_autoscaling_group" "asg" {
    desired_capacity          = 2
    health_check_grace_period = 3600
    health_check_type         = "EC2"
    launch_configuration      = aws_launch_configuration.launch_config.name
    max_size                  = 2
    min_size                  = 1
    name                      = "asg-cd-3"
    vpc_zone_identifier       = ["subnet-2489f269", "subnet-d41fa9f5"]

}

# Create Application Load Balancer
resource "aws_alb" "lb" {
    idle_timeout    = 60
    internal        = false
    load_balancer_type = "application"
    name            = "redirect-load-balancer-3"
    security_groups = [aws_security_group.sg.id]
    subnets         = ["subnet-2489f269", "subnet-d41fa9f5"]

    enable_deletion_protection = false
}

# Create Target Group
resource "aws_alb_target_group" "lb_tg" {
  name     = "target-group-3"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.my_vpc_id

  health_check {
    path = "/"
    port = 8000
    healthy_threshold = 5
    unhealthy_threshold = 2
    timeout = 5
    interval = 30
    matcher = "200"  # has to be HTTP 200 or fails
  }
}

# Define attachment between ASG instances and target Group
resource "aws_autoscaling_attachment" "asg_attachment_bar" {
  autoscaling_group_name = aws_autoscaling_group.asg.id
  alb_target_group_arn   = aws_alb_target_group.lb_tg.arn
}

# Define a listener port 80
resource "aws_alb_listener" "lb_tg_attach_80" {
  load_balancer_arn = aws_alb.lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.lb_tg.arn
    type             = "forward"
  }
}

# Define a listener port 443
resource "aws_alb_listener" "lb_tg_attach_443" {
  load_balancer_arn = aws_alb.lb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = "arn:aws:acm:us-east-1:664379268339:certificate/1fbeae97-b384-47dd-8262-b3c08c9081ed"

  default_action {
    target_group_arn = aws_alb_target_group.lb_tg.arn
    type             = "forward"
  }
}

# Create Database
resource "aws_db_instance" "db" {
    identifier                = "database-3"
    allocated_storage         = 20
    storage_type              = "gp2"
    engine                    = "postgres"
    engine_version            = "12.3"
    instance_class            = "db.t2.micro"
    name                      = var.db_name
    username                  = var.db_username
    password                  = var.db_password
    port                      = var.db_port
    publicly_accessible       = true
    availability_zone         = "us-east-1a"
    security_group_names      = []
    vpc_security_group_ids    = [aws_security_group.sg.id]
    db_subnet_group_name      = "default-vpc-34da1d49"
    parameter_group_name      = "default.postgres12"
    multi_az                  = false
    backup_retention_period   = 7
    backup_window             = "06:59-07:29"
    maintenance_window        = "thu:03:09-thu:03:39"
}

# Create S3 Bucket
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "iluovo-chat-assets-3"
  acl    = "private"
}
