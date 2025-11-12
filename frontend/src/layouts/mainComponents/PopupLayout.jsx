function PopupLayout({ children }) {
  return (
    <div
      className="position-absolute bottom-0 start-0 d-flex flex-column justify-content-start align-content-center m-0 p-0"
      style={{
        backgroundColor: "#00000080",
        backdropFilter: "blur(5px)",
        width: "100vw",
        height: "82vh",
      }}
    >
      <div className="d-flex mx-auto h-100 w-100 p-3">{ children }</div>
    </div>
  );
}

export default PopupLayout;
