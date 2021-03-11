import boto3
import csv

s3 = boto3.resource('s3',aws_access_key_id='',aws_secret_access_key=''
	)

try:
        s3.create_bucket(Bucket='kek165', CreateBucketConfiguration={
                'LocationConstraint': 'us-west-2'
        })
except:
        print("this may already exist")

bucket = s3.Bucket('kek165')

bucket.Acl().put(ACL='public-read')

dyndb = boto3.resource('dynamodb',aws_access_key_id='',aws_secret_access_key='', region_name='us-west-2')

try:
        table = dyndb.create_table(
                TableName = 'DataTable',
                KeySchema = [
                        { 'AttributeName': 'PartitionKey', 'KeyType': 'HASH' },
                        { 'AttributeName': 'RowKey', 'KeyType': 'RANGE' }
                        ],
                AttributeDefinitions=[
                        { 'AttributeName': 'PartitionKey', 'AttributeType': 'S' },
                        { 'AttributeName': 'RowKey', 'AttributeType': 'S' }
                        ],
                ProvisionedThroughput={'ReadCapacityUnits': 5,'WriteCapacityUnits': 5}
                )

        table.meta.client.get_waiter('table_exists').wait(TableName='DataTable')
except:
        pass

table = dyndb.Table("DataTable")

urlbase = "https://s3-us-west-2.amazonaws.com/kek165/"
with open(r"C:\Users\Kent\Desktop\CS1660\yup\experiments.csv", 'r') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(csvf)
    for item in csvf:
        body = open(r"C:\Users\Kent\Desktop\CS1660\yup\\"+item[4], 'rb')
        s3.Object('kek165', item[4]).put(Body=body)
        md= s3.Object('kek165', item[4]).Acl().put(ACL='public-read')
        url=urlbase+item[4]
                
        metadata_item={'PartitionKey': item[0], 'RowKey': item[1],
                        'description': item[3], 'date' : item[2], 'url':url}
        print(metadata_item)
        table.put_item(Item=metadata_item)











