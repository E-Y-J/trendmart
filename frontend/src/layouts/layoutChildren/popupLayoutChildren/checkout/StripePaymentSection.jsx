import { useEffect, useState } from 'react';
import { Elements } from '@stripe/react-stripe-js';
import { getStripe } from '../../../../stripe/stripeClients';
import { getStripeConfig, createPaymentIntent } from '@api/payments';
import StripeCardForm from './StripeCardForm';

function StripePaymentSection({ orderId, currency = 'usd', amountCents = 0, onBack, onPaymentComplete }) {
    const [publishableKey, setPublishableKey] = useState(null);
    const [clientSecret, setClientSecret] = useState(null);
    const [loading, setLoading] = useState(true);
    const [err, setErr] = useState(null);

    useEffect(() => {
        (async () => {
            try {
                const cfg = await getStripeConfig();
                setPublishableKey(cfg?.publishableKey || cfg?.publishable_key);
                const intent = await createPaymentIntent(orderId, currency);
                setClientSecret(intent?.client_secret);
                setErr(null);
            } catch (e) {
                setErr('Unable to initialize payment.');
            } finally {
                setLoading(false);
            }
        })();
    }, [orderId, currency]);

    if (loading) return <div>Loading payment…</div>;
    if (err) return <div className="text-danger">{err}</div>;
    if (!publishableKey || !clientSecret) return <div className="text-danger">Missing Stripe configuration.</div>;

    return (
        <Elements stripe={getStripe(publishableKey)} options={{ clientSecret }}>
            <StripeCardForm
                clientSecret={clientSecret}
                currency={currency}
                amountCents={amountCents}
                onBack={onBack}
                onComplete={onPaymentComplete}
            />
        </Elements>
    );
}

export default StripePaymentSection;
