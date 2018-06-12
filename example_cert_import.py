import boto3

client = boto3.client("acm")

response = client.import_certificate(
    CertificateArn='string',
    Certificate=b'bytes',
    PrivateKey=b'bytes',
    CertificateChain=b'bytes'
)

print(response)

