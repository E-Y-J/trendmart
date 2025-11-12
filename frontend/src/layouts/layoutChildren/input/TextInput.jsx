import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";

function TextInput({
  children,
  inputId,
  placeholder,
  onChange,
  disabled = false,
  info = null,
  password = false,
}) {
  return (
    <Form.Group style={{ width: "100%" }} controlId={inputId}>
      <InputGroup>
        <Form.Control
          type={password ? "password" : "text"}
          placeholder={placeholder}
          disabled={disabled}
          onChange={onChange}
          name={inputId}
          autoComplete="on"
        />
        {children}
      </InputGroup>
      {info && (
        <Form.Text
          style={{ padding: ".1rem 1rem 1rem 1rem", marginBottom: "1rem" }}
        >
          <em>{info}</em>
        </Form.Text>
      )}
    </Form.Group>
  );
}

export default TextInput;
