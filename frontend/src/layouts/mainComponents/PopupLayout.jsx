function PopupLayout({ children }) {
  return (
    <div
      className="position-absolute bottom-0 start-0 d-flex flex-column justify-content-center align-content-center m-0 p-0"
      style={{
        backgroundColor: '#00000080',
        backdropFilter: 'blur(5px)',
        width: '100vw',
        height: '82vh',
      }}
    >
      <div
        className="d-flex bg-light mx-auto"
        style={{
          width: 'fit-content',
        }}
      >
        {children}
      </div>
    </div>
  );
}

export default PopupLayout;