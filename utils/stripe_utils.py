"""
@file-overview This module provides utility functions for handling Stripe payment intents in the Dreamer Document AI project.
@filepath utils/stripe_utils.py
"""

import os
import stripe
from app import app

stripe.api_key = app.config["STRIPE_SECRET_KEY"]


def create_payment_intent(amount, currency="cny"):
    """
    Create a payment intent for document analysis.

    Args:
        amount (int): The amount to charge in the smallest currency unit (e.g., cents).
        currency (str): The currency code (default is 'cny').

    Returns:
        stripe.PaymentIntent: The created payment intent object.

    Raises:
        stripe.error.StripeError: If there is an error creating the payment intent.
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={"enabled": True},
            payment_method_configuration=app.config["STRIPE_PAYMENT_METHOD_CONFIG"],
            metadata={"service": "document_analysis"},
        )
        return intent
    except stripe.error.StripeError as e:
        app.logger.error(f"Stripe error: {str(e)}")
        raise e


def confirm_payment_intent(payment_intent_id):
    """
    Confirm a payment intent.

    Args:
        payment_intent_id (str): The ID of the payment intent to confirm.

    Returns:
        stripe.PaymentIntent: The confirmed payment intent object.

    Raises:
        stripe.error.StripeError: If there is an error retrieving the payment intent.
    """
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent
    except stripe.error.StripeError as e:
        app.logger.error(f"Stripe error: {str(e)}")
        raise e
