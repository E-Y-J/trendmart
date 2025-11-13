import CloseButton from 'react-bootstrap/CloseButton';

function PopupCloseButton({ onClick }) {
  return (
    <CloseButton
      className="position-absolute top-0 end-0"
      style={{ zIndex: 999 }}
      onClick={onClick}
    />
  );
}

export default PopupCloseButton;
