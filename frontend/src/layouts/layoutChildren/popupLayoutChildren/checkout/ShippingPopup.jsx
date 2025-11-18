import Card from 'react-bootstrap/Card';
import { useNavigate } from 'react-router-dom';
import PopupCloseButton from '@children/button/CloseButton';
import { useTheme } from '@styles/themeContext';
import ShippingAddressForm from './ShippingAddressForm';

function ShippingPopup() {
    const { theme } = useTheme();
    const navigate = useNavigate();

    return (
        <Card className='p-3 shadow position-relative m-auto'
            style={{
                width: '100%',
                height: '100%',
                backgroundColor: '#fffffb',
                color: '#222',
                borderRadius: 4,
                ...theme.schemes.darkText,
            }}
        >
            <PopupCloseButton onClick={() => navigate(-1)} />
            <Card.Body className='h-100 d-flex flex-column gap-3'>
                <h3 className='m-0'>Shipping Address</h3>
                <ShippingAddressForm
                    onBack={() => navigate(-1)}
                    onNext={() => { navigate(-1); }} // this is for testing purposes only will change to navigate to /checkout/payment/${orderId}
                />
            </Card.Body>
        </Card>
    );
}

export default ShippingPopup;