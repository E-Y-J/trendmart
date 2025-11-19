import { Container, Row, Col, Nav, Tab, Form, Button, Spinner } from 'react-bootstrap';
import { useState, useEffect, use } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setStatus, clearStatus } from '@redux/status/statusSlice';
import { getCurrentUser, getAddresses, addAddress, deleteAddress, setDefaultAddress } from '@api/customer';

const Address = () => {
   
    const dispatch = useDispatch();
    const { user, isAuthenticated, token } = useSelector((state) => state.auth);
    
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [authUser, setAuthUser] = useState(null);

    const [addressInfo, setAddressInfo] = useState({
        line1: '',
        line2: '',
        city: '',
        state: '',
        zip_code  : '',
        country: ''
    });

    const handleChangeAddress = (e) => {
        const { name, value } = e.target;
        setAddressInfo(prev => ({
        ...prev,
        [name]: value
        }));
    };

   

    useEffect(() => {
        if(user){
            setAuthUser(user);
        }
    }, [user]);


    useEffect(() => {
        const fetchAddresses = async () => {
        try {
            const addresses = await getAddresses();
            if (addresses.length > 0) {
            const primaryAddress = addresses.find(addr => addr.is_default) || addresses[0];
            setAddressInfo({
                line1: primaryAddress.line1 || '',
                line2: primaryAddress.line2 || '',  
                city: primaryAddress.city || '',
                state: primaryAddress.state || '',
                zip_code: primaryAddress.zip_code || '',
                country: primaryAddress.country || ''
            });
            }
        } catch (err) {
            console.error('Error fetching addresses:', err);
        }
        };

        fetchAddresses();
    }, [dispatch]);

    const handleSubmitAddress = async (e) => {
        e.preventDefault();
        setSaving(true);
        dispatch(clearStatus());
        try {
            await addAddress(addressInfo);
            dispatch(setStatus({ message: 'Address saved successfully.', variant: 'success' }));
        } catch (err) {
            console.error('Error saving address:', err);
            dispatch(setStatus({ message: 'Failed to save address.', variant: 'error' }));
        } finally {
            setSaving(false);
        }
    };

  return (
    <>
        <h4>Address Information</h4>
        <p>{authUser ? `Logged in as: ${authUser.email}` : 'Not logged in'}</p>
        <Form onSubmit={handleSubmitAddress}>
            <Row>
                <Col>
                    <Form.Group className="mb-3">
                        <Form.Label>Line 1</Form.Label>
                        <Form.Control type="text" onChange={handleChangeAddress} name="line1" value={addressInfo.line1} placeholder="Enter street address" />
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3">
                        <Form.Label>Line 2</Form.Label>
                        <Form.Control type="text" onChange={handleChangeAddress} name="line2" value={addressInfo.line2} placeholder="Apt, Suite, etc. (optional)" />
                    </Form.Group>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Form.Group className="mb-3">
                        <Form.Label>City</Form.Label>
                        <Form.Control type="text" onChange={handleChangeAddress} name="city" value={addressInfo.city} placeholder="Enter city" />
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3">
                        <Form.Label>State</Form.Label>
                        <Form.Control type="text" onChange={handleChangeAddress} name="state" value={addressInfo.state} placeholder="Enter state" />
                    </Form.Group>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Form.Group className="mb-3">
                    <Form.Label>ZIP Code</Form.Label>
                    <Form.Control type="text" onChange={handleChangeAddress} name="zip_code" value={addressInfo.zip_code} placeholder="Enter ZIP code" />
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3">
                    <Form.Label>Country</Form.Label>
                    <Form.Control type="text" onChange={handleChangeAddress} name="country" value={addressInfo.country} placeholder="Enter country" />
                    </Form.Group>
                </Col>
            </Row>
            <Button variant="primary" type="submit"> Save Address</Button>
        </Form>
    </>
   
  );

}

export default Address;
