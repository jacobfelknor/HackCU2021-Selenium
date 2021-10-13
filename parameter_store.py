import boto3

# SSM region
REGION = "us-west-2"


# Function for get_parameters
def get_parameters_aws(param_key):
    ssm = boto3.client("ssm", region_name=REGION)
    response = ssm.get_parameters(
        Names=[
            param_key,
        ],
        WithDecryption=True,
    )
    return response["Parameters"][0]["Value"]
