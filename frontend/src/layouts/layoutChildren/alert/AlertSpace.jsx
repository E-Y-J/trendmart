import Alert from 'react-bootstrap/Alert';
import CloseButton from 'react-bootstrap/CloseButton';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import { useDispatch } from 'react-redux';
import { clearStatus } from '@redux/status/statusSlice';

function AlertSpace({ alertMessage, variant = 'success' }) {
  const dispatch = useDispatch();

  return (
    <Alert
      key={variant}
      variant={variant === 'error' ? 'danger' : variant}
      className="h-100 m-0 p-0 w-100 justify-content-center align-items-center"
      style={{
        height: '6vh',
        display: 'flex',
        color: '#0a1f44',
      }}
    >
      <Row className="w-100 d-flex flex-row">
        <Col className="flex-grow-1">{alertMessage}</Col>
        <Col className="d-flex flex-column align-self-end flex-grow-0">
          <CloseButton onClick={() => dispatch(clearStatus())} />
        </Col>
      </Row>
    </Alert>
  );
}

export default AlertSpace;
