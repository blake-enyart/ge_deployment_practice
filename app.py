#!/usr/bin/env python3

from aws_cdk import core

from infrastructure.infrastructure_stack import InfrastructureStack


app = core.App()
InfrastructureStack(app, "infrastructure", env={"region": "us-east-1"})

app.synth()
