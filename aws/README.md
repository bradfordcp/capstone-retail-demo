# Installer AWS Provider

    vagrant plugin install vagrant-aws

# Clear Living Nodes

    vagrant destroy -f

# Start AWS Nodes

    vagrant up --provider aws dev0
    
# Find IP Address

    vagrant awsinfo -m dev0 -k public_ip

# SSH into Node

    vagrant ssh dev0

# Grab all IPs

    vagrant awsinfo -m dev0 -k public_ip
    vagrant awsinfo -m dev1 -k public_ip
    vagrant awsinfo -m dev2 -k public_ip
    vagrant awsinfo -m dev3 -k public_ip
    vagrant awsinfo -m dev4 -k public_ip
    vagrant awsinfo -m dev5 -k public_ip
    vagrant awsinfo -m dev6 -k public_ip
    vagrant awsinfo -m dev7 -k public_ip
    vagrant awsinfo -m dev8 -k public_ip
    vagrant awsinfo -m dev9 -k public_ip
    vagrant awsinfo -m dev10 -k public_ip
    vagrant awsinfo -m dev11 -k public_ip
    vagrant awsinfo -m dev12 -k public_ip
    vagrant awsinfo -m dev13 -k public_ip
    vagrant awsinfo -m dev14 -k public_ip
    vagrant awsinfo -m dev15 -k public_ip
    vagrant awsinfo -m dev16 -k public_ip
    vagrant awsinfo -m dev17 -k public_ip
    vagrant awsinfo -m dev18 -k public_ip
    vagrant awsinfo -m dev19 -k public_ip
    vagrant awsinfo -m dev20 -k public_ip
