import datetime
import json
from behave import given, when, then


@given("policy for user {external_user_id} with benefit {benefit} for max total amount of {amount:g} {currency}")
def step_impl(context, external_user_id, benefit, amount, currency):
    response = context.client.post(
        "/policy/",
        {
            "external_user_id": external_user_id,
            "benefit": benefit,
            "total_max_amount": amount,
            "currency": currency,
        },
    )
    if response.status_code != 201:
        raise ValueError("Policy wasn't created: {}".format(response.content))


@when("a payment is received from {external_user_id} for benefit {benefit} with amount {amount:g} {currency}")
def step_impl(context, external_user_id, benefit, amount, currency):
    context.payment_response_data = context.client.post(
        "/payment/",
        {
            "external_user_id": external_user_id,
            "benefit": benefit,
            "amount": amount,
            "currency": currency,
            "timestamp": datetime.datetime.utcnow().isoformat(),
        },

    )


@then("the payment was {successful_or_unsuccessful}")
def step_impl(context, successful_or_unsuccessful):
    context.payment_response_data = json.loads(context.payment_response_data.content.decode("utf-8"))
    if context.payment_response_data.get("authorized") is not (successful_or_unsuccessful == "successful"):
        raise ValueError("Payment wasn't {}: {}".format(successful_or_unsuccessful, context.payment_response_data))


@then("the payment declination reason was {reason}")
def step_impl(context, reason):
    if not context.payment_response_data.get("reason") == reason:
        raise ValueError(
            "Payment declination reason is not {}, but {}".format(reason, context.payment_response_data.get("reason"))
        )
