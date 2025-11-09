import Alert from "react-bootstrap/Alert";

function AlertSpace({ alertMessage, variant = "success" }) {
  return (
    <Alert
    key={variant}
    variant={variant === "error" ? "danger" : variant}
    className="h-100 m-0 p-0 w-100 justify-content-center align-items-center"
      style={{
        height: '6vh',
        display: "flex",
        color: "#0a1f44",
      }}
      dismissible
    >
      {alertMessage}
    </Alert>
  );
}

export default AlertSpace;
