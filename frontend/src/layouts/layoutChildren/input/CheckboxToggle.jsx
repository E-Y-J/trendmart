import Form from "react-bootstrap/Form";
import Stack from "react-bootstrap/Stack";

function CheckboxToggle({ onClick, checked }) {
  return (
    <Stack
      id="toggleContainer"
      direction="horizontal"
      gap={3}
      style={{
        justifyContent: "space-around",
        alignItems: "center",
        position: "relative",
        borderRadius: ".4rem",
        backgroundImage: "linear-gradient(to bottom, #f3f3ea, #f0f0f0)",
        boxShadow: "0 1px 1px rgb(255 255 255 / .6)",
        fontSize: "1rem",
        height: "auto",
        padding: "0.5rem 1rem",
      }}
    >
      <h4
        style={{
          color: checked ? "#00aef0" : "#0a1f44",
          opacity: checked ? 0.6 : 1,
          fontWeight: checked ? 500 : 700,
          transform: checked ? "scale(0.9)" : "scale(1.05)",
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
          fontWeight: checked ? 700 : 500,
          transform: checked ? "scale(1.05)" : "scale(0.9)",
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
