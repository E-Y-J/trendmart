import stripe
from flask import current_app
from models.payment import Payment
from models.shopping import Order
from extensions import db
from datetime import datetime


class PaymentService:
    """
    Handles all the Stripe payment stuff for our e-commerce app.

    This class basically wraps all the Stripe API calls and manages our 
    payment records in the database. I tried to keep it simple but still 
    handle all the edge cases we might run into.
    """

    @staticmethod
    def create_payment_intent(order_id, amount, currency='usd', metadata=None):
        """
        Creates a Stripe PaymentIntent for an order.

        This is the first step in our payment flow - we create the intent on our 
        backend, then send the client_secret to the frontend so they can confirm 
        the payment with Stripe.js.

        Args:
            order_id: The ID of the order we're creating payment for
            amount: Payment amount in cents (so $19.99 = 1999)
            currency: Three-letter currency code, defaults to USD  
            metadata: Any extra data we want to store with the payment

        Returns:
            Dictionary with client_secret (for frontend), payment_intent_id, 
            and our internal payment_id

        Note: This creates a pending Payment record in our DB right away, even 
        before the customer actually pays. The webhook will update the status later.
        """
        try:
            # Check if order exists first
            order = Order.query.get(order_id)
            if not order:
                raise ValueError(f"Order {order_id} not found")

            # Make sure we don't double-charge
            if order.payment:
                raise ValueError(f"Order {order_id} already has a payment")

            # Setup metadata for tracking
            payment_metadata = {
                'order_id': str(order_id),
                'integration': 'trendmart'
            }
            if metadata:
                payment_metadata.update(metadata)

            # Create the Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                automatic_payment_methods={'enabled': True},
                metadata=payment_metadata
            )

            # Save payment info to our database
            payment = Payment(
                order_id=order_id,
                total_amount=amount / 100,
                currency=currency.upper(),
                payment_method='card',  # Will update this later when we know the actual method
                stripe_payment_intent_id=intent.id,
                status='pending'
            )

            db.session.add(payment)
            db.session.commit()

            return {
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'payment_id': payment.id
            }

        except stripe.error.StripeError as e:
            db.session.rollback()
            current_app.logger.error(f"Stripe API error: {e}")
            raise
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Payment creation failed: {e}")
            raise

    @staticmethod
    def confirm_payment(payment_intent_id):
        """
        Updates our payment record when Stripe confirms (or fails) a payment.

        This gets called either manually or from our webhook handler. It checks 
        the current status of a PaymentIntent in Stripe and updates our database 
        to match. Pretty straightforward but important for keeping everything in sync.

        Args:
            payment_intent_id: The Stripe PaymentIntent ID we want to check

        Returns:
            The updated Payment object from our database

        Note: If the payment succeeded, we also try to grab the actual payment 
        method that was used (card, apple_pay, etc.) and store that too.
        """
        try:
            # Get the payment intent from Stripe
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Find our payment record
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=payment_intent_id
            ).first()

            if not payment:
                raise ValueError(
                    f"Can't find payment for intent {payment_intent_id}")

            # Update status based on what happened
            if intent.status == 'succeeded':
                payment.status = 'completed'
                payment.paid_at = datetime.utcnow()
                # Try to get the actual payment method used
                if intent.charges.data:
                    payment.payment_method = intent.charges.data[0].payment_method_details.type
            elif intent.status == 'payment_failed':
                payment.status = 'failed'
            elif intent.status == 'canceled':
                payment.status = 'canceled'
            else:
                # Just use whatever Stripe says
                payment.status = intent.status

            db.session.commit()
            return payment

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to confirm payment: {e}")
            raise

    @staticmethod
    def process_webhook_event(event):
        """
        Processes incoming webhook events from Stripe.

        Stripe sends us webhooks whenever something happens with a payment - 
        succeeded, failed, canceled, etc. This method looks at the event type 
        and calls the right handler to update our payment records.

        Args:
            event: The webhook event data from Stripe (already parsed JSON)

        Returns:
            True if we handled the event successfully, False if something went wrong

        Note: We only handle the payment_intent events we care about. Other 
        event types just get logged and ignored for now. Might expand this later 
        if we need to handle refunds, disputes, etc.
        """
        try:
            # Handle the webhook events we care about
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                PaymentService.confirm_payment(payment_intent['id'])
            elif event['type'] == 'payment_intent.payment_failed':
                payment_intent = event['data']['object']
                PaymentService.confirm_payment(payment_intent['id'])
            elif event['type'] == 'payment_intent.canceled':
                payment_intent = event['data']['object']
                PaymentService.confirm_payment(payment_intent['id'])
            else:
                # Log unhandled events but don't fail
                current_app.logger.info(
                    f"Got unhandled event: {event['type']}")

            return True
        except Exception as e:
            current_app.logger.error(f"Webhook processing failed: {e}")
            return False

    @staticmethod
    def get_payment_status(payment_id):
        """
        Gets the current status and details of a payment.

        Simple helper method to fetch payment info. Usually called by API 
        endpoints when the frontend wants to check on a payment status, or 
        for admin dashboards to see payment details.

        Args:
            payment_id: Our internal payment ID (not the Stripe one)

        Returns:
            Dictionary with all the important payment details formatted nicely 
            for API responses. Dates are converted to ISO format strings.

        Raises:
            ValueError if the payment doesn't exist in our database
        """
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        # Return the payment data as a dict
        return {
            'id': payment.id,
            'status': payment.status,
            'total_amount': payment.total_amount,
            'currency': payment.currency,
            'payment_method': payment.payment_method,
            'created_at': payment.created_at.isoformat(),
            'paid_at': payment.paid_at.isoformat() if payment.paid_at else None
        }
