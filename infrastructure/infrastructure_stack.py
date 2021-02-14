from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
)

from aws_solutions_constructs import aws_cloudfront_s3 as cloudfront_s3
from typing_extensions import runtime


class InfrastructureStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(
            self, "s3Bucket", removal_policy=core.RemovalPolicy.DESTROY
        )
        core.CfnOutput(
            self,
            "s3BucketName",
            value=s3_bucket.bucket_name,
        )

        edge_func = _lambda.Function(
            self,
            "edgeLambda",
            runtime=_lambda.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=_lambda.Code.from_inline(
                """
                'use strict';
                exports.handler = (event, context, callback) => {

                    // Get request and request headers
                    const request = event.Records[0].cf.request;
                    const headers = request.headers;

                    // Configure authentication
                    const authUser = 'user';
                    const authPass = 'pass';

                    // Construct the Basic Auth string
                    const authString = 'Basic ' + new Buffer(authUser + ':' + authPass).toString('base64');

                    // Require Basic authentication
                    if (typeof headers.authorization == 'undefined' || headers.authorization[0].value != authString) {
                        const body = 'Unauthorized';
                        const response = {
                            status: '401',
                            statusDescription: 'Unauthorized',
                            body: body,
                            headers: {
                                'www-authenticate': [{key: 'WWW-Authenticate', value:'Basic'}]
                            },
                        };
                        callback(null, response);
                    }

                    // Continue request processing if authentication passed
                    callback(null, request);
                };"""
            ),
        )

        cf_dist = cloudfront.Distribution(
            self,
            "cloudfrontDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(s3_bucket),
                edge_lambdas=[
                    cloudfront.EdgeLambda(
                        event_type=cloudfront.LambdaEdgeEventType.VIEWER_REQUEST,
                        function_version=edge_func.current_version,
                    )
                ],
            ),
            default_root_object="index.html",
        )

        # cf_s3 = cloudfront_s3.CloudFrontToS3(
        #     self,
        #     "cloudfrontS3",
        #     cloud_front_distribution_props=cf_props,
        #     existing_bucket_obj=s3_bucket,
        # )
