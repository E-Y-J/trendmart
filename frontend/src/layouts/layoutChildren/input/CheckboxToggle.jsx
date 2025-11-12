import Form from "react-bootstrap/Form";
import Stack from "react-bootstrap/Stack";

function CheckboxToggle({ onClick, checked }) {
  return (
    <Stack
      id="toggleContainer"
      direction="horizontal"
      className="d-flex flex-row justify-content-around align-items-center position-relative gap-3"
      gap={3}
      style={{
        borderRadius: ".4rem",
        boxShadow: "0 1px 1px rgb(255 255 255 / .6)",
        fontSize: "1rem",
        padding: "0.5rem 1rem",
      }}
    >
      <h4
        style={{
          color: checked ? "#00aef0" : "#0a1f44",
          opacity: checked ? 0.6 : 1,
          transition: "all 0.3s ease",
          margin: 0,
        }}
      >
        Login
      </h4>

      <Form.Check
        type="switch"
        id="custom-switch"
        checked={checked}
        onChange={onClick}
        style={{
          transform: "scale(1.5)",
          accentColor: checked ? "#00aef0" : "#0a1f44",
          cursor: "pointer",
        }}
      />

      <h4
        style={{
          color: checked ? "#00aef0" : "#0a1f44",
          opacity: checked ? 1 : 0.6,
          transition: "all 0.3s ease",
          margin: 0,
        }}
      >
        Register
      </h4>
    </Stack>
  );
}

export default CheckboxToggle;
