import { Container, Row, Col, Nav, Tab, Form, Button, Spinner } from 'react-bootstrap';
import { useState, useEffect, use } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setStatus, clearStatus } from '@redux/status/statusSlice';
import { useTheme } from '@styles/themeContext';
import { getCurrentUser, getProfile, upsertProfile, getAddresses, addAddress, deleteAddress, setDefaultAddress } from '@api/customer';
import Address from './Address';

const Profile = () => {
  const { user, isAuthenticated, token, status: authStatus } = useSelector((state) => state.auth);
  const { theme } = useTheme();
  const dispatch = useDispatch();
  const [contactInfo, setContactInfo] = useState({
    first_name: '',
    last_name: '',
    phone: ''
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const fetchCurrentUser = async () => {
    try {
      const user = await getCurrentUser();
      console.log('Current user fetched:', user);
      return user;
    } catch (err) {
      console.error('Error fetching current user:', err);
      return null;
    }
  };

  // Fetch user data when component mounts
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        setLoading(true);
        dispatch(clearStatus()); 
        
        const userProfile = await getProfile();
   
        // Update form with fetched data
        setContactInfo({
          first_name: userProfile.first_name || '',
          last_name: userProfile.last_name || '',
          phone: userProfile.phone || '',
        });
        
        dispatch(setStatus({
          message: 'Profile loaded successfully!',
          variant: 'success'
        }));
      } catch (err) {
        console.error('Error fetching user data:', err);
        dispatch(setStatus({
          message: 'Failed to load profile data. Please try again.',
          variant: 'error'
        }));
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [dispatch]);

  

  const handleChange = (e) => {
    const { name, value } = e.target;
    setContactInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Clear any previous status messages
    dispatch(clearStatus());
    
    // Basic validation
    if (!contactInfo.first_name.trim() || !contactInfo.last_name.trim()) {
      dispatch(setStatus({
        message: 'Please fill in both first name and last name.',
        variant: 'error'
      }));
      return;
    }

    try {
      setSaving(true);
      
      dispatch(setStatus({
        message: 'Saving profile changes...',
        variant: 'info'
      }));
      
      await upsertProfile(contactInfo);
      
      dispatch(setStatus({
        message: 'Profile updated successfully!',
        variant: 'success'
      }));
      
      console.log('Profile saved successfully:', contactInfo);
    } catch (err) {
      console.error('Error saving profile:', err);
      dispatch(setStatus({
        message: 'Failed to save profile changes. Please try again.',
        variant: 'error'
      }));
    } finally {
      setSaving(false);
    }
  };
  
  return (
    <Col
      className="d-inline-flex flex-column position-relative justify-content-between align-items-center gap-1 px-2 py-4 m-auto w-100"
      style={{
        ...theme.schemes.darkText,
        borderRadius: theme.props.bR_less,
        filter: 'drop-shadow(.5rem .5rem 1rem #0a1f44e8)'
      }}
    >
      <Row className="h-100 w-100 justify-content-center  my-auto">

      <h3 className="mb-4">Profile</h3>
     
        <Tab.Container id="left-tabs-example" defaultActiveKey="contactInfo">
          {/* Tab Navigation - Responsive */}
          <Col xs={12} md={3} className="mb-3 mb-md-0">
            <Nav variant="pills" className="flex-row flex-md-column justify-content-center">
              <Nav.Item className="flex-fill flex-md-grow-0">
                <Nav.Link 
                  eventKey="contactInfo"
                  className="text-center text-md-start"
                  style={{ fontSize: 'clamp(0.8rem, 2vw, 1rem)' }}
                >
                  <span className="d-md-none">Contact</span>
                  <span className="d-none d-md-inline">Contact Information</span>
                </Nav.Link>
              </Nav.Item>
              <Nav.Item className="flex-fill flex-md-grow-0">
                <Nav.Link 
                  eventKey="address"
                  className="text-center text-md-start"
                  style={{ fontSize: 'clamp(0.8rem, 2vw, 1rem)' }}
                >
                  Address
                </Nav.Link>
              </Nav.Item>
              <Nav.Item className="flex-fill flex-md-grow-0">
                <Nav.Link 
                  eventKey="security"
                  className="text-center text-md-start"
                  style={{ fontSize: 'clamp(0.8rem, 2vw, 1rem)' }}
                >
                  Security
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>

          {/* Tab Content */}
          <Col xs={12} md={9} className="p-3 p-md-4 bg-light">
            <Tab.Content className="p-3 rounded">
              <Tab.Pane eventKey="contactInfo">
                <h4>Contact Information</h4>
                <Form className="mt-3" onSubmit={handleSubmit}>
                  <Form.Group className="mb-3" controlId="firstName">
                    <Form.Label>First Name</Form.Label>
                    <Form.Control 
                      type="text"
                      name="first_name" 
                      value={contactInfo.first_name}
                      onChange={handleChange} 
                      placeholder="Enter first name" 
                    />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="lastName">
                    <Form.Label>Last Name</Form.Label>
                    <Form.Control 
                      type="text" 
                      name="last_name"
                      value={contactInfo.last_name}
                      onChange={handleChange} 
                      placeholder="Enter last name" 
                    />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="phone">
                    <Form.Label>Phone Number</Form.Label>
                    <Form.Control 
                      type="tel" 
                      name="phone"
                      value={contactInfo.phone}
                      onChange={handleChange} 
                      placeholder="Enter phone number" 
                    />
                  </Form.Group>

                  <Button 
                    variant="primary" 
                    type="submit"
                    disabled={saving}
                    className="d-flex align-items-center gap-2"
                  >
                    {saving && (
                      <Spinner 
                        animation="border" 
                        size="sm"
                        role="status"
                      />
                    )}
                    {saving ? 'Saving...' : 'Save Changes'}
                  </Button>
                </Form>
              </Tab.Pane>

               <Tab.Pane eventKey="address">
                <Address />
              </Tab.Pane>

              <Tab.Pane eventKey="security">
                <h4>Security Settings</h4>
                <Form>
                  <Form.Group className="mb-3">
                    <Form.Label>Current Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter current password" />
                  </Form.Group>
                  <Form.Group className="mb-3">
                    <Form.Label>New Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter new password" />
                  </Form.Group>
                  <Form.Group className="mb-3">
                    <Form.Label>Confirm New Password</Form.Label>
                    <Form.Control type="password" placeholder="Confirm new password" />
                  </Form.Group>
                  <Button variant="primary" type="submit">
                    Change Password
                  </Button>
                </Form>
              </Tab.Pane> 
            </Tab.Content>
          </Col>
          
        </Tab.Container>
        </Row>
      </Col>
      
   
  );

}

export default Profile;
