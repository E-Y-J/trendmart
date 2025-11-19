import { useEffect, useMemo, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { getAddresses, setDefaultAddress, addAddress } from '@api/customer';
import { useTheme } from '@styles/themeContext';

function ShippingAddressForm({ onNext, onBack }) {
    const { theme } = useTheme();
    const [loading, setLoading] = useState(true);
    const [addresses, setAddresses] = useState([]);
    const [selected, setSelected] = useState(null);
    const [useNew, setUseNew] = useState(false);
    const [newAddress, setNewAddress] = useState({ line1: '', line2: '', city: '', state: '', zip_code: '', country: 'USA' });

    const US_STATES = useMemo(() => ([
        { abbr: 'AL', name: 'Alabama' }, { abbr: 'AK', name: 'Alaska' }, { abbr: 'AZ', name: 'Arizona' }, { abbr: 'AR', name: 'Arkansas' },
        { abbr: 'CA', name: 'California' }, { abbr: 'CO', name: 'Colorado' }, { abbr: 'CT', name: 'Connecticut' }, { abbr: 'DE', name: 'Delaware' },
        { abbr: 'FL', name: 'Florida' }, { abbr: 'GA', name: 'Georgia' }, { abbr: 'HI', name: 'Hawaii' }, { abbr: 'ID', name: 'Idaho' },
        { abbr: 'IL', name: 'Illinois' }, { abbr: 'IN', name: 'Indiana' }, { abbr: 'IA', name: 'Iowa' }, { abbr: 'KS', name: 'Kansas' },
        { abbr: 'KY', name: 'Kentucky' }, { abbr: 'LA', name: 'Louisiana' }, { abbr: 'ME', name: 'Maine' }, { abbr: 'MD', name: 'Maryland' },
        { abbr: 'MA', name: 'Massachusetts' }, { abbr: 'MI', name: 'Michigan' }, { abbr: 'MN', name: 'Minnesota' }, { abbr: 'MS', name: 'Mississippi' },
        { abbr: 'MO', name: 'Missouri' }, { abbr: 'MT', name: 'Montana' }, { abbr: 'NE', name: 'Nebraska' }, { abbr: 'NV', name: 'Nevada' },
        { abbr: 'NH', name: 'New Hampshire' }, { abbr: 'NJ', name: 'New Jersey' }, { abbr: 'NM', name: 'New Mexico' }, { abbr: 'NY', name: 'New York' },
        { abbr: 'NC', name: 'North Carolina' }, { abbr: 'ND', name: 'North Dakota' }, { abbr: 'OH', name: 'Ohio' }, { abbr: 'OK', name: 'Oklahoma' },
        { abbr: 'OR', name: 'Oregon' }, { abbr: 'PA', name: 'Pennsylvania' }, { abbr: 'RI', name: 'Rhode Island' }, { abbr: 'SC', name: 'South Carolina' },
        { abbr: 'SD', name: 'South Dakota' }, { abbr: 'TN', name: 'Tennessee' }, { abbr: 'TX', name: 'Texas' }, { abbr: 'UT', name: 'Utah' },
        { abbr: 'VT', name: 'Vermont' }, { abbr: 'VA', name: 'Virginia' }, { abbr: 'WA', name: 'Washington' }, { abbr: 'WV', name: 'West Virginia' },
        { abbr: 'WI', name: 'Wisconsin' }, { abbr: 'WY', name: 'Wyoming' }
    ]), []);

    const load = async () => {
        setLoading(true);
        try {
            const data = await getAddresses();
            const list = Array.isArray(data) ? data : [];
            setAddresses(list);
            if (list.length === 0) {
                setUseNew(true);
            }
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { load(); }, []);

    const onSubmit = async (e) => {
        e.preventDefault();
        if (useNew) {
            const created = await addAddress({
                line1: newAddress.line1,
                line2: newAddress.line2,
                city: newAddress.city,
                state: newAddress.state,
                zip_code: newAddress.zip_code,
                country: newAddress.country,
            });
            if (created?.id) await setDefaultAddress(created.id);
        } else if (selected) {
            await setDefaultAddress(selected);
        }
        onNext?.();
    };

    const canContinue = useMemo(() => (
        useNew
            ? Boolean(newAddress.line1 && newAddress.city && newAddress.state && newAddress.zip_code)
            : Boolean(selected)
    ), [useNew, newAddress.line1, newAddress.city, newAddress.state, newAddress.zip_code, selected]);

    return (
        <Form className='d-flex flex-column gap-3' onSubmit={onSubmit} style={{ maxWidth: 520, margin: '0 auto' }}>
            <h5 className='mb-1'>Shipping Address</h5>
            {loading ? (
                <div>Loading addresses…</div>
            ) : (
                <>
                    <div className='d-flex flex-column gap-2'>
                        {addresses.length > 0 && addresses.map((a) => (
                            <Form.Check
                                key={a.id}
                                type='radio'
                                name='address'
                                id={`address-${a.id}`}
                                label={`${a.line1}, ${a.city}, ${a.state} ${a.zip_code}`}
                                checked={!useNew && selected === a.id}
                                onChange={() => { setUseNew(false); setSelected(a.id); }}
                            />
                        ))}
                        <Form.Check
                            type='radio'
                            name='addr'
                            id='address-new'
                            label='Use a new address'
                            checked={useNew}
                            onChange={() => { setUseNew(true); setSelected(null); }}
                        />
                    </div>

                    {useNew && (
                        <div className='d-flex flex-column gap-2'>
                            <Form.Control placeholder='Address line 1' value={newAddress.line1} onChange={(e) => setNewAddress({ ...newAddress, line1: e.target.value })} />
                            <Form.Control placeholder='Address line 2 (optional)' value={newAddress.line2} onChange={(e) => setNewAddress({ ...newAddress, line2: e.target.value })} />

                            <Row className='g-2'>
                                <Col md={6}>
                                    <Form.Control placeholder='City' value={newAddress.city} onChange={(e) => setNewAddress({ ...newAddress, city: e.target.value })} />
                                </Col>
                                <Col md={6}>
                                    <Form.Select
                                        aria-label='Select state'
                                        value={newAddress.state}
                                        onChange={(e) => setNewAddress({ ...newAddress, state: e.target.value })}
                                    >
                                        <option value="">Select state</option>
                                        {US_STATES.map((s) => (
                                            <option key={s.abbr} value={s.abbr}>{s.name} ({s.abbr})</option>
                                        ))}
                                    </Form.Select>
                                </Col>
                            </Row>

                            <Form.Control placeholder='ZIP Code' value={newAddress.zip_code} onChange={(e) => setNewAddress({ ...newAddress, zip_code: e.target.value })} />
                            <Form.Control placeholder='Country' value={newAddress.country} onChange={(e) => setNewAddress({ ...newAddress, country: e.target.value })} />
                        </div>
                    )}

                    <div className='d-flex justify-content-between mt-2'>
                        <Button variant='outline-secondary' onClick={onBack} style={{ ...theme.buttons?.muted }}>Back</Button>
                        <Button type='submit' variant='dark' style={{ ...theme.buttons?.splash }} disabled={!canContinue}>Continue to Payment</Button>
                    </div>
                </>
            )}
        </Form>
    );
}

export default ShippingAddressForm;