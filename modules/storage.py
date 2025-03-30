"""
S3 storage resources for Pulumi AWS ESC demo
"""
import pulumi
import pulumi_aws as aws

def create_bucket():
    """
    Create an S3 bucket using configuration from Pulumi ESC
    """
    config = pulumi.Config()
    region = config.get("awsRegion")
    bucket_prefix = config.get("bucketPrefix") or "esc-demo-"
    
    # Create AWS provider with configured region
    aws_provider = aws.Provider("aws-storage-provider", region=region)
    
    # Create the S3 bucket
    bucket = aws.s3.Bucket("demo-bucket",
        bucket_prefix=bucket_prefix,
        acl="private",
        versioning=aws.s3.BucketVersioningArgs(
            enabled=True,
        ),
        opts=pulumi.ResourceOptions(provider=aws_provider)
    )
    
    return bucket
