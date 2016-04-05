# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):


    dynamodb = boto3.resource('dynamodb')
    mapTable = dynamodb.Table('device-map')

    try:
        macAddr = event['query']['macAddr']
    except KeyError:
        pass
    else:
        macAddrLookUp = mapTable.get_item(
            Key={
                'macAddr': macAddr
            }
        )

        if 'Item' not in macAddrLookUp:
            print("macAddrLookUp output: ", macAddrLookUp['ResponseMetadata'])
            return {"message": "MAC not found."}
        else:
            return { "macAddr": macAddrLookUp['Item']['macAddr'], "deviceId": macAddrLookUp['Item']['deviceId']}

    try:
        deviceId = event['query']['deviceId']
    except KeyError:
        pass
    else:
        deviceIdLookUp = mapTable.scan(
            FilterExpression=Attr('deviceId').eq(deviceId)
        )

        if 'Items' not in deviceIdLookUp:
            print("deviceIdLookUp output: ", deviceIdLookUp['ResponseMetadata'])
            return {"message": "DeviceId not found."}
        else:
            return { "macAddr": deviceIdLookUp['Items'][0]['macAddr'], "deviceId": deviceIdLookUp['Items'][0]['deviceId']}