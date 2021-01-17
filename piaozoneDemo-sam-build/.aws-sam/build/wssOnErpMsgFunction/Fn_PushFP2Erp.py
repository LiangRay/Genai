import json
import boto3
import os

#apiEndPointUrl = "https://mkhp953pk8.execute-api.us-east-2.amazonaws.com/production"
apiEndPointUrl = os.environ['ERP_CONNECT_ENDPOINT']
print(apiEndPointUrl)
apiClient = boto3.client('apigatewaymanagementapi', endpoint_url=apiEndPointUrl)

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('piaozone')
    
    userid = event["userid"]
    response = table.get_item( Key={
            'userid': userid
        }
    )
    print(response)
    fapiao = response['Item'].get('FapiaoInfo', 'Please upload new Fapiao')
    print(fapiao)
    connectionId = response['Item']['erpconnectid']
    #信息回传
    print(connectionId)
    response = apiClient.post_to_connection(
        Data=f'Fapio Info: {fapiao}'.encode('ascii'),
        ConnectionId=connectionId
    )
    
    
    return {
        "userid":userid
    }
