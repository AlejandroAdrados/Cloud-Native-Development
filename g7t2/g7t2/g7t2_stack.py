import os

from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as api_gateway,
    aws_cognito as cognito,
    aws_s3 as s3,
    aws_lambda_event_sources as event_source,
    Tags,
    Duration,
    CfnOutput,
)
from aws_cdk.aws_apigateway import LambdaIntegration
from constructs import Construct
from .constructs.queued_lambda import QueuedLambda


class G7T2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # environment variables
        env = {}

        # dynamodb table
        table = dynamodb.Table(
            self,
            "assignments",
            partition_key=dynamodb.Attribute(
                name="UserId", type=dynamodb.AttributeType.STRING
            ),
            table_name="assignments",
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
        )
        env["TABLE_NAME"] = table.table_name

        # cognito user pool
        pool = cognito.UserPool(
            self,
            "user_pool",
            user_pool_name="user_pool",
            sign_in_aliases=cognito.SignInAliases(email=True),
            standard_attributes=cognito.StandardAttributes(
                family_name=cognito.StandardAttribute(
                    required=True, mutable=False
                ),
                given_name=cognito.StandardAttribute(
                    required=True, mutable=False
                ),
            ),
            custom_attributes={"profile_picture": cognito.StringAttribute()},
            self_sign_up_enabled=True,
        )

        pool_client = pool.add_client(
            "pool-client",
            user_pool_client_name="g7t2-auth-client",
            auth_flows=cognito.AuthFlow(user_password=True, custom=True),
        )

        api_authorizer = api_gateway.CognitoUserPoolsAuthorizer(
            self, "api-authorizer", cognito_user_pools=[pool]
        )

        # S3
        profile_pic_bucket = s3.Bucket(
            self, "profile_picture_bucket", bucket_name="profile-picture"
        )

        addition_generator = QueuedLambda(
            self,
            "addition-generator",
            "addition-generation",
            lambda_.Code.from_asset("lambdas"),
            "generators/addition.handle",
            environment=env,
        )

        multiplication_generator = QueuedLambda(
            self,
            "multiplication_generator",
            "multiplication-generation",
            lambda_.Code.from_asset("lambdas"),
            "generators/multiplication.handle",
            environment=env,
        )

        derivatives_generator = QueuedLambda(
            self,
            "derivatives-generator",
            "derivatives-generation",
            lambda_.Code.from_asset("lambdas"),
            "generators/derivatives.handle",
            environment=env,
        )

        addition_evaluator = QueuedLambda(
            self,
            "addition-evaluator",
            "addition-evaluation",
            lambda_.Code.from_asset("lambdas"),
            "evaluators/addition.handle",
            environment=env,
            function_name="addition-evaluator",
        )

        multiplication_evaluator = QueuedLambda(
            self,
            "multiplication-evaluator",
            "multiplication-evaluation",
            lambda_.Code.from_asset("lambdas"),
            "evaluators/multiplication.handle",
            environment=env,
            function_name="multiplication-evaluator",
        )

        derivates_evaluator = QueuedLambda(
            self,
            "derivation-evaluator",
            "derivation-evaluation",
            lambda_.Code.from_asset("lambdas"),
            "evaluators/derivatives.handle",
            environment=env,
            function_name="derivation-evaluator",
        )

        # statistics lambda
        profile_lambda = lambda_.Function(
            self,
            "ProfileLambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="statistics/get_profile.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment=env,
            function_name="profile-lambda",
        )

        # watcher lambda
        watcher_lambda = lambda_.Function(
            self,
            "watcher_lambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="dynamo_watchers/regenerate_exercises.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={
                "TOPIC_ADD": addition_generator.topic.topic_arn,
                "TOPIC_MULT": multiplication_generator.topic.topic_arn,
                "TOPIC_DERIV": derivatives_generator.topic.topic_arn,
                "TABLE_NAME": table.table_name,
            },
            function_name="watcher-lambda",
        )

        # grant permission to statistics lambda to write to assignments table
        table.grant_full_access(profile_lambda)
        table.grant_full_access(watcher_lambda)

        generators = [
            addition_generator,
            multiplication_generator,
            derivatives_generator,
        ]

        evaluators = [
            addition_evaluator,
            multiplication_evaluator,
            derivates_evaluator,
        ]

        post_sign_up_lambda = lambda_.Function(
            self,
            "post-sign-up-lambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="cognito_triggers/post_sign_up.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name="post-sign-up-lambda",
            environment={
                "topic_arns": ",".join(
                    generator.topic.topic_arn for generator in generators
                ),
                "TABLE_NAME": table.table_name,
            },
        )

        # Give sign-up-trigger permission to publish to topic
        for generator in generators:
            generator.topic.grant_publish(post_sign_up_lambda)
            generator.topic.grant_publish(watcher_lambda)
            table.grant_full_access(generator.lambda_)

        pool.add_trigger(
            cognito.UserPoolOperation.POST_CONFIRMATION,
            post_sign_up_lambda,  # type: ignore
        )

        # connect dynamodb stream to watcher lambda
        watcher_lambda.add_event_source(
            event_source.DynamoEventSource(
                table=table,
                starting_position=lambda_.StartingPosition.TRIM_HORIZON,
            )
        )

        # get exercise lambda
        get_exercise_lambda = lambda_.Function(
            self,
            "GetExerciseLambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="coordinators/get_exercise.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name="exercise-lambda",
            environment=env,
        )

        # post solution lambda
        post_solution_lambda = lambda_.Function(
            self,
            "PostSolutionLambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="coordinators/post_solution.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name="solution-lambda",
            environment={
                "ADD_EVAL": addition_evaluator.topic.topic_arn,
                "MULT_EVAL": multiplication_evaluator.topic.topic_arn,
                "DERIV_EVAL": derivates_evaluator.topic.topic_arn,
            },
        )

        for evaluator in evaluators:
            evaluator.topic.grant_publish(post_solution_lambda)
            table.grant_full_access(evaluator.lambda_)

        # test lambda function
        test_lambda = lambda_.Function(
            self,
            "test-lambda",
            code=lambda_.Code.from_asset("lambdas"),
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="test_lambda.handle",
            environment={"TABLE_NAME": table.table_name},
            function_name="test-lambda",
        )
        table.grant_full_access(test_lambda)

        sign_up_lambda = lambda_.Function(
            self,
            "SignUpLambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="auth/custom_sign_up.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name="SignUpLambda",
            environment={
                "COGNITO_CLIENT_ID": pool_client.user_pool_client_id,
                "PROFILE_PICUTRE_BUCKET_NAME": profile_pic_bucket.bucket_name,
            },
            timeout=Duration.seconds(20),
        )

        confirmation_lambda = lambda_.Function(
            self,
            "ConfirmationLambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="auth/confirm_user.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name="ConfirmationLambda",
            environment={"COGNITO_CLIENT_ID": pool_client.user_pool_client_id},
            timeout=Duration.seconds(10),
        )

        login_lambda = lambda_.Function(
            self,
            "LoginLambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="auth/login.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name="LoginLambda",
            environment={"COGNITO_CLIENT_ID": pool_client.user_pool_client_id},
            timeout=Duration.seconds(10),
        )

        email_trigger_lambda = lambda_.Function(
            self,
            "EmailTriggerLambda",
            code=lambda_.Code.from_asset("lambdas"),
            handler="auth/email_trigger.handle",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name="EmailTriggerLambda",
            timeout=Duration.seconds(10),
            environment={
                "FRONTEND_URL": os.environ.get(
                    "FRONTEND_URL", "http://127.0.0.1:3000"
                )
            },
        )

        pool.add_trigger(
            cognito.UserPoolOperation.CUSTOM_MESSAGE,
            email_trigger_lambda,  # type: ignore
        )

        api = api_gateway.RestApi(
            self,
            "Api",
            default_cors_preflight_options=api_gateway.CorsOptions(
                allow_origins=api_gateway.Cors.ALL_ORIGINS,
                allow_methods=api_gateway.Cors.ALL_METHODS,
            ),
        )
        Tags.of(api).add("_custom_id_", "g7t2API")

        auth = api.root.add_resource("auth")
        auth.add_method(
            "POST",
            integration=LambdaIntegration(sign_up_lambda),  # type: ignore
        )

        confirm = auth.add_resource("confirm")
        confirm.add_method(
            "POST",
            integration=LambdaIntegration(confirmation_lambda),  # type: ignore
        )

        login = auth.add_resource("login")
        login.add_method(
            "POST", integration=LambdaIntegration(login_lambda)  # type: ignore
        )

        profile_api = api.root.add_resource("profile")
        # TODO: Add authorizers, responses, request templates
        profile_api.add_method(
            "GET",
            integration=LambdaIntegration(
                profile_lambda,  # type: ignore
            ),
            authorizer=api_authorizer,
        )

        exercise_api = api.root.add_resource("exercise")
        exercise_api.add_method(
            "GET",
            integration=LambdaIntegration(get_exercise_lambda),  # type: ignore
            authorizer=api_authorizer,
        )

        solution_api = exercise_api.add_resource("solution")
        solution_api.add_method(
            "POST",
            integration=LambdaIntegration(post_solution_lambda),  # type: ignore # noqa
            authorizer=api_authorizer,
        )

        CfnOutput(
            self,
            "USER-POOL-CLIENT-ID",
            value=pool_client.user_pool_client_id,
            export_name="USER_POOL_CLIENT_ID",
        )

        health = api.root.add_resource("health")
        health.add_method("GET")
