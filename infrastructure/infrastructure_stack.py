from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    core,
)

from aws_solutions_constructs import aws_cloudfront_s3 as cloudfront_s3


class InfrastructureStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cloudfront_s3.CloudFrontToS3(
            self,
            "cloudfrontS3",
        )
