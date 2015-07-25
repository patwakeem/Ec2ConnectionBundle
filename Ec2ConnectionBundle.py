"""
Author: Patrick W.
Date: 4/30/15

Requires: boto

This class creates connections to each aws region and provides an easy interface to get the connection or loop through all ec2 regions.

Example Usgae:

Instantiate class:

ec2Connect = Ec2ConnectionBundle('API KEY', 'API SECRET')

Loop through ec2 connections:

for regionConnection in ec2Connect.generateConnections():
    #do stuff

Loop through ec2 connections excluding a certain region:

for regionConnection in ec2Connect.generateConnections(excludeRegion='us-west-1'):
    #do stuff

Get a single ec2 connection:

usWestConnection = ec2Connect.getSingleConnection('us-west-1')

"""
import boto.ec2

class Ec2ConnectionBundle(object):

    def __init__(self, access_key, secret_key):
        self.aws_access_key = access_key
        self.aws_secret_key = secret_key
        self.regions = ["us-east-1", "us-west-2", "us-west-1", "eu-west-1", "eu-central-1", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "sa-east-1"]
        self.ec2GlobalDictionary = {}

        for region in self.regions:
            try:
                self.ec2GlobalDictionary[region] = boto.ec2.connect_to_region(region, aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key)
            except:
                print("There was a problem connecting to AWS using your credentials in region: " + region)

    def getSingleConnection(self, region):
        if region in self.regions:
            return self.ec2GlobalDictionary[region]
        else:
            return None

    def generateConnections(self, excludeRegion=None):

        if excludeRegion is None:
            for region in self.regions:
                yield self.ec2GlobalDictionary[region]

        else:
            for region in self.regions:
                if region != excludeRegion:
                    yield self.ec2GlobalDictionary[region]
