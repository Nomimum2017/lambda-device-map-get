# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)

import boto3

def lambda_handler(event, context):

    if event['query']['macAddr']:
        macAddr = event['query']['macAddr']
    elif event['query']['deviceId']:
        deviceId = event['query']['deviceId']

    dynamodb = boto3.resource('dynamodb')
    mapTable = dynamodb.Table('device-map')

    macAddrLookUp = mapTable.get_item(
        Key={
            'macAddr': macAddr
        }
    )

    deviceIdLookUp = mapTable.get_item(
        Key={
            'deviceId': deviceId
        }
    )

    if 'Item' not in macAddrLookUp:
        print("macAddrLookUp output: ", macAddrLookUp['ResponseMetadata'])
        return { "message": "MAC not found." }

    if 'Item' not in deviceIdLookUp:
        print("deviceIdLookUp output: ", deviceIdLookUp['ResponseMetadata'])
        return {"message": "DeviceId not found."}

    return