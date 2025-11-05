function AlertSpace({ alertMessage, variant='success'|'error'|'info' }) {

  const alertType = {
    success: '#00aef0',
    error: '#be4748',
    info: '#f3f3ea'
  };

  return (
    <div
      id="alertSpace"
      style={{
        flexGrow: 1,
        height: '100%',
        alignContent: 'center',
        backgroundColor: `${alertType[variant] || 'none'}`,
        textAlign: 'center',
        fontWeight: 600,
        color: '#0a1f44',
      }}
    >
      { alertMessage }
    </div>
  );
}

export default AlertSpace;