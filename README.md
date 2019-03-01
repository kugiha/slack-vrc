# slack-vrc
Slack bot for VRC

`fsf` fetches data via the VRChat API and store them to DynamoDB. It should be invoked with decent intervals.    
`sp` retrieve data from DynamoDB, invoked by users slack commands, which does not call the VRChat API directly.

## Feature
- /vrc online: list your online friends
- /vrc ong: list your online friends with instance-id-based groups
### WIP
- Send a notification when your favorite user logs in. (WIP)

## Libs

The following libraries are used in this repository.

- vrchat-api-python-master
- slackbot

## Usage
Detailed instructions are now WIP.
### fsf
1. Upload `fsf.zip` as AWS lambda function with Python 3.
1. Set CloudWatch Events with sufficient intervals.
1. Set env variables (TODO)
### sp
1. Upload `fsf.zip` as AWS lambda function with Python 3.
1. Set API Gateway.
1. Set env variables (TODO)

## Contribution

Fork this repository and create pull request.
