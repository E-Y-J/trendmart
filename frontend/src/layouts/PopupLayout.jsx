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
          
          border: '2px solid #212529', 
          borderRadius: '0.5rem', 
          boxShadow: '0 1rem 3rem rgba(0,0,0,0.175)', 
          padding: '1.5rem', 
          margin: '1.5rem', 
          maxWidth: '90vw',
          maxHeight: '90vh',
          overflowY: 'auto',
        }}
      >
        { children ? children : <Outlet/> }
      </div>
    </div>
  );
}

export default PopupLayout;
