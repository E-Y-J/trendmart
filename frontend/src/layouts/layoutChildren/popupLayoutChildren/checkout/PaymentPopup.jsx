import Card from 'react-bootstrap/Card';
import { useNavigate, useParams } from 'react-router-dom';
import PopupCloseButton from '@children/button/CloseButton';
import { useTheme } from '@styles/themeContext';
import StripePaymentSection from './StripePaymentSection';

function PaymentPopup() {
    const { theme } = useTheme();
    const navigate = useNavigate();
    const { orderId } = useParams();

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
                <h3 className='m-0'>Payment</h3>
                <StripePaymentSection
                    onBack={() => navigate(-1)}
                    onNext={() => { navigate(-1); }} // this is for testing purposes only will change to navigate to /checkout/confirmation/${orderId}
                />
            </Card.Body>
        </Card>
    )
};

export default PaymentPopup;