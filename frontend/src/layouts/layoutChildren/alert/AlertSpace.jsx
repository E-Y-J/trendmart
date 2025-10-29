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
        width: '98%',
        height: '8vh',
        alignContent: 'center',
        margin: '1%',
        backgroundColor: `${alertType[variant] || '#00000000'}`,
        textAlign: 'center',
        color: 'wheat'
      }}
    >
      <div style={{ height: '100%' }}>

      { alertMessage }
      </div>
    </div>
  );
}

export default AlertSpace;