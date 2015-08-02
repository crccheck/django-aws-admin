from aws_admin.utils import pull_ec2, pull_security_groups


if __name__ == '__main__':
    import django; django.setup()
    if 1:
        pull_ec2()
    pull_security_groups()
