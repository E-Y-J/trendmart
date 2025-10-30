function PopupLayout({ children }) {
  return (
    <>
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          backgroundColor: '#00000080',
          backdropFilter: 'blur(5px)',
          width: '100vw',
          height: 'calc(100vh - 18vh - 4%)',
          alignContent: 'center',
          justifyContent: 'center',
          display: 'flex',
          overflowY: 'auto',
        }}
      >
        <div style={{backgroundColor: '#fffffb', display: 'flex', width: 'fit-content', margin: 'auto' }} >
          { children }
        </div>
      </div>
    </>
  );
}

export default PopupLayout;
