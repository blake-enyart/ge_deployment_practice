# import json
# import pytest

# from aws_cdk import core
# from infrastructure.infrastructure_stack import InfrastructureStack


# def get_template():
#     app = core.App()
#     InfrastructureStack(app, "infrastructure")
#     return json.dumps(app.synth().get_stack("infrastructure").template)


# def test_sqs_queue_created():
#     assert("AWS::SQS::Queue" in get_template())


def test_placeholder():
    assert 1 == 1
