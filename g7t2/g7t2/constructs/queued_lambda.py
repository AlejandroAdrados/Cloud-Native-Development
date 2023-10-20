from typing import Optional, Any

from constructs import Construct
from aws_cdk import (
    aws_lambda as lambda_,
    aws_sns as sns,
    aws_sqs as sqs,
    aws_sns_subscriptions as sns_subs,
    aws_lambda_event_sources as lambda_event_sources,
)


class QueuedLambda(Construct):
    """
    A SNS-SQS-Lambda construct.

    SQS subscribed to SNS and calling lambda when message is available.
    ---------
    Attribute:
        - topic: The SNS topic of this construct.
        - queue: The SQS queue of this construct.
        - lambda_: The Lambda of this construct.
    """

    def __init__(
        self,
        scope: "Construct",
        id: str,
        topic_name: str,
        lambda_dir: lambda_.AssetCode,
        lambda_handler: str,
        runtime: lambda_.Runtime = lambda_.Runtime.PYTHON_3_9,
        function_name: Optional[str] = None,
        environment: Optional["dict[str, Any]"] = None,
    ) -> None:
        """
        Creates a new SNS-SQS-Lambda construct.
        ------
        Params:
            - required:
                - scope: The scope of this construct.
                - id: The id of this construct.
                - topic_name: The name for the SNS topic.
                - lambda_dir: The asset code of the lambda.
                - lambda_handler: The handler of the lambda.
            - optional:
                - runtime: The runtime of the handler (default: PYTHON_3_9)
        """
        super().__init__(scope, id)

        self.lambda_ = lambda_.Function(
            self,
            f"{id}-lambda",
            runtime=runtime,
            code=lambda_dir,
            handler=lambda_handler,
            function_name=function_name,
            environment=environment,
        )

        self.topic = sns.Topic(
            self,
            f"{id}-topic",
            topic_name=topic_name,
        )

        self.queue = sqs.Queue(self, f"{id}-queue")
        self.topic.add_subscription(sns_subs.SqsSubscription(self.queue))

        event_source = lambda_event_sources.SqsEventSource(self.queue)
        self.lambda_.add_event_source(event_source)
