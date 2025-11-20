import { Container, Row, Col, Nav, Tab, Form, Button, Spinner, Card, Badge } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setStatus, clearStatus } from '@redux/status/statusSlice';
import { getCurrentUser, getAddresses, addAddress, deleteAddress, setDefaultAddress } from '@api/customer';

const Address = () => {
   
    const dispatch = useDispatch();
    const { user, isAuthenticated, token } = useSelector((state) => state.auth);
    
    const [addresses, setAddresses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [showAddForm, setShowAddForm] = useState(false);
    const [authUser, setAuthUser] = useState(null);


    const [newAddress, setNewAddress] = useState({
        line1: '',
        line2: '',
        city: '',
        state: '',
        zip_code: '',
        country: ''
    });

    const handleChangeAddress = (e) => {
        const { name, value } = e.target;
        setNewAddress(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const resetForm = () => {
        setNewAddress({
            line1: '',
            line2: '',
            city: '',
            state: '',
            zip_code: '',
            country: ''
        });
        setShowAddForm(false);
    };

    const handleShowAddForm = () => {
        setShowAddForm(true);  
    };

    useEffect(() => {
        if(user){
            setAuthUser(user);
        }
    }, [user]);


    useEffect(() => {
        const fetchAddresses = async () => {
            try {
                setLoading(true);
                const addressesData = await getAddresses();
                setAddresses(addressesData || []);
                
                dispatch(setStatus({ 
                    message: `Found ${addressesData?.length || 0} saved addresses.`, 
                    variant: 'info' 
                }));
            } catch (err) {
                console.error('Error fetching addresses:', err);
                dispatch(setStatus({ 
                    message: 'Failed to load addresses.', 
                    variant: 'error' 
                }));
            } finally {
                setLoading(false);
            }
        };

        fetchAddresses();
    }, [dispatch]);

    const handleSubmitAddress = async (e) => {
        e.preventDefault();
        setSaving(true);
        dispatch(clearStatus());
        
        try {
            await addAddress(newAddress);
            dispatch(setStatus({ 
                message: 'Address saved successfully!', 
                variant: 'success' 
            }));
            
            // Refresh addresses list
            const updatedAddresses = await getAddresses();
            setAddresses(updatedAddresses || []);
            
            // Reset form and hide it
            resetForm();
        } catch (err) {
            console.error('Error saving address:', err);
            dispatch(setStatus({ 
                message: 'Failed to save address.', 
                variant: 'error' 
            }));
        } finally {
            setSaving(false);
        }
    };

    const handleDeleteAddress = async (addressId) => {
        if (!window.confirm('Are you sure you want to delete this address?')) {
            return;
        }

        try {
            await deleteAddress(addressId);
            dispatch(setStatus({ 
                message: 'Address deleted successfully!', 
                variant: 'success' 
            }));
            
            // Refresh addresses list
            const updatedAddresses = await getAddresses();
            setAddresses(updatedAddresses || []);
        } catch (err) {
            console.error('Error deleting address:', err);
            dispatch(setStatus({ 
                message: 'Failed to delete address.', 
                variant: 'error' 
            }));
        }
    };

    const handleSetDefault = async (addressId) => {
        try {
            await setDefaultAddress(addressId);
            dispatch(setStatus({ 
                message: 'Default address updated!', 
                variant: 'success' 
            }));
            
            // Refresh addresses list
            const updatedAddresses = await getAddresses();
            setAddresses(updatedAddresses || []);
        } catch (err) {
            console.error('Error setting default address:', err);
            dispatch(setStatus({ 
                message: 'Failed to set default address.', 
                variant: 'error' 
            }));
        }
    };

    // Show loading spinner while fetching data
    if (loading) {
        return (
            <div className="d-flex justify-content-center align-items-center" style={{ height: '200px' }}>
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading addresses...</span>
                </Spinner>
            </div>
        );
    }

    return (
        <>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h4>My Addresses</h4>
                {!showAddForm && (
                    <Button 
                        variant="primary" 
                        onClick={handleShowAddForm}
                        className="d-flex align-items-center gap-2"
                    >
                        <i className="fas fa-plus"></i>
                        Add New Address
                    </Button>
                )}
            </div>

            {showAddForm && (
                <Card className="mt-4" >
                    <Card.Header className="d-flex justify-content-between align-items-center">
                        <h5 className="mb-0">Add New Address</h5>
                        <Button 
                            variant="outline-secondary" 
                            size="sm"
                            onClick={resetForm}
                        >
                            Cancel
                        </Button>
                    </Card.Header>
                    <Card.Body>
                        <Form onSubmit={handleSubmitAddress}>
                            <Row>
                                <Col md={6}>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Street Address *</Form.Label>
                                        <Form.Control 
                                            type="text" 
                                            name="line1" 
                                            value={newAddress.line1}
                                            onChange={handleChangeAddress} 
                                            placeholder="Enter street address"
                                            required
                                        />
                                    </Form.Group>
                                </Col>
                                <Col md={6}>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Apt, Suite, etc. (optional)</Form.Label>
                                        <Form.Control 
                                            type="text" 
                                            name="line2" 
                                            value={newAddress.line2}
                                            onChange={handleChangeAddress} 
                                            placeholder="Apartment, suite, unit, etc."
                                        />
                                    </Form.Group>
                                </Col>
                            </Row>
                            
                            <Row>
                                <Col md={4}>
                                    <Form.Group className="mb-3">
                                        <Form.Label>City *</Form.Label>
                                        <Form.Control 
                                            type="text" 
                                            name="city" 
                                            value={newAddress.city}
                                            onChange={handleChangeAddress} 
                                            placeholder="Enter city"
                                            required
                                        />
                                    </Form.Group>
                                </Col>
                                <Col md={4}>
                                    <Form.Group className="mb-3">
                                        <Form.Label>State *</Form.Label>
                                        <Form.Control 
                                            type="text" 
                                            name="state" 
                                            value={newAddress.state}
                                            onChange={handleChangeAddress} 
                                            placeholder="Enter state"
                                            required
                                        />
                                    </Form.Group>
                                </Col>
                                <Col md={4}>
                                    <Form.Group className="mb-3">
                                        <Form.Label>ZIP Code *</Form.Label>
                                        <Form.Control 
                                            type="text" 
                                            name="zip_code" 
                                            value={newAddress.zip_code}
                                            onChange={handleChangeAddress} 
                                            placeholder="Enter ZIP code"
                                            required
                                        />
                                    </Form.Group>
                                </Col>
                            </Row>
                            
                            <Row>
                                <Col md={6}>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Country *</Form.Label>
                                        <Form.Control 
                                            type="text" 
                                            name="country" 
                                            value={newAddress.country}
                                            onChange={handleChangeAddress} 
                                            placeholder="Enter country"
                                            required
                                        />
                                    </Form.Group>
                                </Col>
                            </Row>
                            
                            <div className="d-flex gap-2">
                                <Button 
                                    variant="primary" 
                                    type="submit"
                                    disabled={saving}
                                    className="d-flex align-items-center gap-2"
                                >
                                    {saving && <Spinner animation="border" size="sm" />}
                                    {saving ? 'Saving...' : 'Save Address'}
                                </Button>
                                <Button 
                                    variant="outline-secondary" 
                                    type="button"
                                    onClick={resetForm}
                                >
                                    Cancel
                                </Button>
                            </div>
                        </Form>
                    </Card.Body>
                </Card>
            )}

           
            {addresses.length > 0 ? (
                <Row className="g-3 mb-4">
                    {addresses.map((address, index) => (
                        <Col md={6} lg={4} key={address.id || index}>
                            <Card className="h-100 position-relative">
                                {address.is_default && (
                                    <Badge 
                                        bg="primary" 
                                        className="position-absolute top-0 start-0 m-2"
                                    >
                                        Default
                                    </Badge>
                                )}
                                
                                <Card.Body>
                                    <Card.Title className="fs-6 mb-3">
                                        Address {index + 1}
                                    </Card.Title>
                                    
                                    <Card.Text className="mb-2">
                                        <strong>{address.line1}</strong><br/>
                                        {address.line2 && <>{address.line2}<br/></>}
                                        {address.city}, {address.state} {address.zip_code}<br/>
                                        {address.country}
                                    </Card.Text>
                                    
                                    <div className="d-flex gap-2 flex-wrap">
                                        {!address.is_default && (
                                            <Button 
                                                variant="outline-primary" 
                                                size="sm"
                                                onClick={() => handleSetDefault(address.id)}
                                            >
                                                Set Default
                                            </Button>
                                        )}
                                        <Button 
                                            variant="outline-danger" 
                                            size="sm"
                                            onClick={() => handleDeleteAddress(address.id)}
                                        >
                                            Delete
                                        </Button>
                                    </div>
                                </Card.Body>
                            </Card>
                        </Col>
                    ))}
                </Row>
            ) : (
                <div className="text-center py-5">
                    <i className="fas fa-map-marker-alt fa-3x text-muted mb-3"></i>
                    <h5 className="text-muted">No addresses found</h5>
                    <p className="text-muted">Add your first address to get started.</p>
                </div>
            )}

            
            
        </>
    );

}

export default Address;
