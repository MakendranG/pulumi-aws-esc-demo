"""
Database resources for Pulumi AWS ESC demo
"""
import pulumi
import pulumi_aws as aws

def create_rds_instance():
    """
    Create an RDS MySQL instance using configuration from Pulumi ESC
    """
    config = pulumi.Config()
    region = config.get("awsRegion")
    db_password = config.get_secret("dbPassword")
    db_instance_class = config.get("dbInstanceClass") or "db.t3.micro"
    
    # Create AWS provider with configured region
    aws_provider = aws.Provider("aws-db-provider", region=region)
    
    # Create a security group for the RDS instance
    security_group = aws.ec2.SecurityGroup("rds-security-group",
        description="Allow MySQL access",
        ingress=[
            {
                "protocol": "tcp",
                "from_port": 3306,
                "to_port": 3306,
                "cidr_blocks": ["0.0.0.0/0"],
            }
        ],
        egress=[
            {
                "protocol": "-1",
                "from_port": 0,
                "to_port": 0,
                "cidr_blocks": ["0.0.0.0/0"],
            }
        ],
        opts=pulumi.ResourceOptions(provider=aws_provider)
    )
    
    # Create the RDS instance
    rds_instance = aws.rds.Instance(
        "demo-rds-instance",
        allocated_storage=20,
        engine="mysql",
        engine_version="8.0",
        instance_class=db_instance_class,
        username="admin",
        password=db_password,
        vpc_security_group_ids=[security_group.id],
        skip_final_snapshot=True,
        publicly_accessible=True,
        parameter_group_name="default.mysql8.0",
        opts=pulumi.ResourceOptions(provider=aws_provider)
    )
    
    return rds_instance
