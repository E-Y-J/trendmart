function PopupLayout({ children }) {
  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          backgroundColor: '#00000080',
          backdropFilter: 'blur(5px)',
          width: '100vw',
          height: 'calc(100vh - 18vh - 2%)',
          alignContent: 'center',
          justifyContent: 'center',
          display: 'flex',
          overflowY: 'auto',
        }}
      >
        { children ? children : <Outlet/> }
      </div>
    </div>
  );
}

export default PopupLayout;
