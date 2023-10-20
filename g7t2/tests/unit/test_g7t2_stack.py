import aws_cdk as core
import aws_cdk.assertions as assertions

from g7t2.g7t2.g7t2_stack import G7T2Stack


# example tests. To run these tests, uncomment this file along with the example
# resource in g7t2/g7t2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = G7T2Stack(app, "g7t2")
    assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
