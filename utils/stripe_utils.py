import os
import stripe
from app import app

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')

def create_payment_intent(amount, currency='usd'):
    """Create a payment intent for document analysis."""
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['card'],
            metadata={'service': 'document_analysis'}
        )
        return intent
    except stripe.error.StripeError as e:
        app.logger.error(f"Stripe error: {str(e)}")
        raise e

def confirm_payment_intent(payment_intent_id):
    """Confirm a payment intent."""
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent
    except stripe.error.StripeError as e:
        app.logger.error(f"Stripe error: {str(e)}")
        raise e
