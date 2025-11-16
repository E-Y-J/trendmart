// Checkout API clients
// Endpoint: POST /checkout/validate (jwt)
//validates the current user's cart before payment processing


import api from './api';

// Validate the current user's cart for checkout
export async function validateCheckout() {
    const { data } = await api.get('/checkout/validate');
    return data;
}

// Safe wrapper for validateCheckout with error handling
export async function safeValidateCheckout() {
    try {
        const data = await validateCheckout();
        return { data, error: null };
    } catch (error) {
        const res = err?.response;
        return {
            data: res?.data || null,
            error:
                res?.data?.error ||
                res?.data?.message ||
                err?.message ||
                'Checkout validation failed',
        };
    }
}