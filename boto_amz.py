import boto3
import sys
import socket
ip_value = socket.gethostbyname('le.petcdocoe.com')

client = boto3.client("route53")


dns_action = client.change_resource_record_sets(
    HostedZoneId='ZIT5N9SUPV5FZ',
    ChangeBatch={
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': sys.argv[1],
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
