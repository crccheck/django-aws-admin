from aws_admin.utils import pull_vpcs, pull_ec2, pull_security_groups


if __name__ == '__main__':
    import django; django.setup()
    pull_vpcs()
    pull_ec2()
    pull_security_groups()
