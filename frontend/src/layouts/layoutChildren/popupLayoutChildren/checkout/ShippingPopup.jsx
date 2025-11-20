import Card from 'react-bootstrap/Card';
import { useNavigate } from 'react-router-dom';
import PopupCloseButton from '@children/button/CloseButton';
import { useTheme } from '@styles/themeContext';
import ShippingAddressForm from './ShippingAddressForm';
import { createOrder } from '@api/orders';

function ShippingPopup() {
    const { theme } = useTheme();
    const navigate = useNavigate();

    return (
        <Card className='p-3 shadow position-relative m-auto'
            style={{
                width: 'min(92vw, 640px)',
                maxHeight: '90vh',
                backgroundColor: '#fffffb',
                color: '#222',
                borderRadius: 4,
                ...theme.schemes.darkText,
            }}
        >
            <PopupCloseButton onClick={() => navigate(-1)} />
            <Card.Body className='d-flex flex-column gap-3' style={{ overflowY: 'auto' }}>
                <h3 className='m-0'>Shipping Address</h3>
                <ShippingAddressForm
                    onBack={() => navigate(-1)}
                    onNext={async () => {
                        try {
                            const res = await createOrder(); // { message, order }
                            const orderId = res?.order?.id || res?.order?._id;
                            if (orderId) navigate(`/checkout/payment/${orderId}`);
                            else navigate(-1);
                        } catch {
                            navigate(-1);
                        }
                    }}
                />
            </Card.Body>
        </Card>
    );
}

export default ShippingPopup;