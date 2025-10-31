function AlertSpace({ alertMessage, variant='success'|'error'|'info' }) {

  const alertType = {
    success: '#008800',
    error: '#880000',
    info: '#000088'
  };

  return (
    <div
      id="alertSpace"
      style={{
        flexGrow: 1,
        height: '100%',
        alignContent: 'center',
        backgroundColor: `${alertType[variant] || '#00000000'}`,
        textAlign: 'center',
        color: 'wheat'
      }}
    >
      { alertMessage }
    </div>
  );
}

export default AlertSpace;