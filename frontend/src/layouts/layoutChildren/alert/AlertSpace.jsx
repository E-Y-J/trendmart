import CloseButton from 'react-bootstrap/CloseButton';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import { useDispatch } from 'react-redux';
import { clearStatus } from '@redux/status/statusSlice';
import { useTheme } from '@styles/themeContext';

function AlertCloseButton({ onClick }) {
  return (
    <CloseButton
      className="position-absolute top-0 end-0"
      style={{
        zIndex: 999,
        transform: 'translate(-50%, 80%)',
      }}
      onClick={onClick}
    />
  )
}

function AlertSpace({ alertMessage, variant }) {
  const { theme } = useTheme();
  const dispatch = useDispatch();
  

  return (
    <Col
      className="h-100 m-0 p-0 w-100 justify-content-center align-items-center position-relative"
      style={{
        height: '6vh',
        display: 'flex',
        color: theme.colors.contrast,
        backgroundColor: theme.alerts[variant],
        borderRadius: `0 0 ${Array(2).fill(theme.props.bR_more).join(' ') }`,
      }}
    >
      <Row className="w-100 d-flex flex-row">
        <Col className="flex-grow-1 justify-content-center align-items-center d-flex">
          <div style={{ ...theme.schemes.darkText, borderRadius: theme.props.bR_less, padding: '.5rem' }}>
            {alertMessage}
          </div>
          <AlertCloseButton onClick={() => dispatch(clearStatus())} />
        </Col>
      </Row>
    </Col>
  );
}

export default AlertSpace;
