#!/usr/bin/env python3
"""
AWS Resource Summary Script
Scans your AWS account and provides a comprehensive summary of resources
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from collections import defaultdict
import json

def get_region():
    """Get the default region from AWS config"""
    try:
        session = boto3.session.Session()
        return session.region_name or 'us-east-1'
    except:
        return 'us-east-1'

def get_all_regions():
    """Get list of all AWS regions"""
    try:
        ec2 = boto3.client('ec2', region_name='us-east-1')
        regions = ec2.describe_regions()['Regions']
        return [region['RegionName'] for region in regions]
    except:
        return ['us-east-1']  # Fallback to default region

def scan_ec2_instances(region):
    """Scan EC2 instances in a region"""
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_instances()

        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                name = 'N/A'
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            name = tag['Value']

                instances.append({
                    'id': instance['InstanceId'],
                    'type': instance['InstanceType'],
                    'state': instance['State']['Name'],
                    'name': name,
                    'region': region
                })
        return instances
    except ClientError as e:
        return []

def scan_s3_buckets():
    """Scan S3 buckets"""
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()

        buckets = []
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']

            # Try to get bucket size
            try:
                cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
                # Note: Getting exact size requires CloudWatch metrics
                buckets.append({
                    'name': bucket_name,
                    'created': bucket['CreationDate'].strftime('%Y-%m-%d')
                })
            except:
                buckets.append({
                    'name': bucket_name,
                    'created': bucket['CreationDate'].strftime('%Y-%m-%d')
                })

        return buckets
    except ClientError:
        return []

def scan_lambda_functions(region):
    """Scan Lambda functions in a region"""
    try:
        lambda_client = boto3.client('lambda', region_name=region)
        response = lambda_client.list_functions()

        functions = []
        for func in response['Functions']:
            functions.append({
                'name': func['FunctionName'],
                'runtime': func['Runtime'],
                'modified': func['LastModified'],
                'region': region
            })
        return functions
    except ClientError:
        return []

def scan_rds_instances(region):
    """Scan RDS instances in a region"""
    try:
        rds = boto3.client('rds', region_name=region)
        response = rds.describe_db_instances()

        databases = []
        for db in response['DBInstances']:
            databases.append({
                'id': db['DBInstanceIdentifier'],
                'engine': db['Engine'],
                'status': db['DBInstanceStatus'],
                'region': region
            })
        return databases
    except ClientError:
        return []

def scan_iam_users():
    """Scan IAM users"""
    try:
        iam = boto3.client('iam')
        response = iam.list_users()

        users = []
        for user in response['Users']:
            users.append({
                'name': user['UserName'],
                'created': user['CreateDate'].strftime('%Y-%m-%d')
            })
        return users
    except ClientError:
        return []

def scan_cloudformation_stacks(region):
    """Scan CloudFormation stacks in a region"""
    try:
        cfn = boto3.client('cloudformation', region_name=region)
        response = cfn.list_stacks(
            StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']
        )

        stacks = []
        for stack in response['StackSummaries']:
            stacks.append({
                'name': stack['StackName'],
                'status': stack['StackStatus'],
                'region': region
            })
        return stacks
    except ClientError:
        return []

def main():
    print("=" * 70)
    print("AWS RESOURCE SUMMARY")
    print("=" * 70)
    print()

    try:
        # Get account info
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"📋 Account ID: {identity['Account']}")
        print(f"👤 User ARN: {identity['Arn']}")
        print()
    except Exception as e:
        print(f"❌ Error getting account info: {e}")
        return

    # Get default region and available regions
    default_region = get_region()
    print(f"🌍 Default Region: {default_region}")
    print()

    # Scan resources (focusing on default region for speed)
    print("Scanning resources in default region...")
    print("-" * 70)

    # S3 Buckets (global)
    print("\n📦 S3 Buckets:")
    buckets = scan_s3_buckets()
    if buckets:
        for bucket in buckets:
            print(f"  • {bucket['name']} (created: {bucket['created']})")
        print(f"  Total: {len(buckets)} bucket(s)")
    else:
        print("  No S3 buckets found")

    # EC2 Instances
    print(f"\n🖥️  EC2 Instances ({default_region}):")
    instances = scan_ec2_instances(default_region)
    if instances:
        for instance in instances:
            print(f"  • {instance['id']} ({instance['type']}) - {instance['state']} - {instance['name']}")
        print(f"  Total: {len(instances)} instance(s)")
    else:
        print("  No EC2 instances found")

    # Lambda Functions
    print(f"\n⚡ Lambda Functions ({default_region}):")
    functions = scan_lambda_functions(default_region)
    if functions:
        for func in functions:
            print(f"  • {func['name']} ({func['runtime']})")
        print(f"  Total: {len(functions)} function(s)")
    else:
        print("  No Lambda functions found")

    # RDS Databases
    print(f"\n🗄️  RDS Databases ({default_region}):")
    databases = scan_rds_instances(default_region)
    if databases:
        for db in databases:
            print(f"  • {db['id']} ({db['engine']}) - {db['status']}")
        print(f"  Total: {len(databases)} database(s)")
    else:
        print("  No RDS databases found")

    # IAM Users
    print("\n👥 IAM Users:")
    users = scan_iam_users()
    if users:
        for user in users:
            print(f"  • {user['name']} (created: {user['created']})")
        print(f"  Total: {len(users)} user(s)")
    else:
        print("  No IAM users found (or no permission)")

    # CloudFormation Stacks
    print(f"\n📚 CloudFormation Stacks ({default_region}):")
    stacks = scan_cloudformation_stacks(default_region)
    if stacks:
        for stack in stacks:
            print(f"  • {stack['name']} - {stack['status']}")
        print(f"  Total: {len(stacks)} stack(s)")
    else:
        print("  No CloudFormation stacks found")

    print("\n" + "=" * 70)
    print("✅ Scan Complete!")
    print("=" * 70)
    print()
    print("💡 Note: This scans only your default region for most services.")
    print("   S3 and IAM are global services and show all resources.")
    print()

if __name__ == "__main__":
    try:
        main()
    except NoCredentialsError:
        print("❌ AWS credentials not found!")
        print("Please configure credentials in ~/.aws/credentials")
    except Exception as e:
        print(f"❌ Error: {e}")
