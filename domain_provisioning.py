#!/usr/bin/python3

#input should be of the form "domain_provisioning.py domain_name"
#eg: domain_provisioning.py rajaram.petcdocoe.com

#codeby:Rajaram Vijayamohan

import os
import time
import boto3
import sys
import subprocess
import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("domain_name", help="Domain will be created based on the input given here")
args = parser.parse_args()

domain = 'le.petcdocoe.com'
zone_id = 'ZIT5N9SUPV5FZ'

ip_value = socket.gethostbyname(domain)
client_route53 = boto3.client("route53")
client_acm = boto3.client("acm")

#getting the domain name as user input and saving it in a variable
domain_name = args.domain_name

#code for configuring a route53 domain
dns_action = client_route53.change_resource_record_sets(
    HostedZoneId=zone_id,
    ChangeBatch={
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': domain_name,
                    'Type': 'A',
                    'TTL': 300,
                    'ResourceRecords': [
                        {
                            'Value': ip_value
                        },
                    ],
                }
            },
        ]
    }
)
print(dns_action)

for i in range(50):
    try:
        socket.gethostbyname(domain_name)
        print("Domain is Up, generating certficates ..")
        break
    except:
        time.sleep(4)
        print(".")
        continue

#getting the cert for the initialized domain
subprocess.call(['sudo','certbot','certonly','--standalone','-d',domain_name])

c = subprocess.check_output(['sudo','cat','/etc/letsencrypt/live/'+domain_name+'/cert.pem'])
p = subprocess.check_output(['sudo','cat','/etc/letsencrypt/live/'+domain_name+'/privkey.pem'])
ch = subprocess.check_output(['sudo','cat','/etc/letsencrypt/live/'+domain_name+'/chain.pem'])

#importing the certificate into aws acm
response = client_acm.import_certificate(
        Certificate=c,
        PrivateKey=p,
        CertificateChain=ch
)

print(response)