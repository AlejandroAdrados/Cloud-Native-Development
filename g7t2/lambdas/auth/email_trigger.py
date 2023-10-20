import os


def handle(event, context):
    print(event)
    if event["triggerSource"] == "CustomMessage_SignUp":
        confirm_link = (
            f"{os.environ['FRONTEND_URL']}"
            + f"/confirm?code={event['request']['codeParameter']}"
            + f"&username={event['userName']}"
        )

        event["response"][
            "emailMessage"
        ] = f"""
          <html>
            <body>
              <h4>Confirm your account</h4>
              <div>Follow the link to confirm your account:
              <a href="{confirm_link}">
                here
              </a>
              </div>
              <div>
                Alternatively, you can manually enter your confirmation code:
                {event['request']['codeParameter']}
              </div>
            </body>
          </html>
        """
        event["response"]["emailSubject"] = "Confirm your account"
    return event
