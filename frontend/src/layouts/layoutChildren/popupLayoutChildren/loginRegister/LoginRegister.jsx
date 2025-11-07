import { useState } from "react";
import { Form, Button, Row, Col } from "react-bootstrap";
import TextInput from "../../input/textInput";
import CheckboxToggle from "../../input/CheckboxToggle";
import PasswordRequirements from "./PasswordRequirements";
import { useNavigate } from "react-router-dom";

function LoginRegister() {
  const [formData, setFormData] = useState({ email: "", password: "", verification: "" });
  const [toggleForm, setToggleForm] = useState("login");
  const [passHidden, setPassHidden] = useState(true);
  const navigate = useNavigate()

  const handleChange = (event) => {
    const { id, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const handleChecked = () => {
    setToggleForm(toggleForm === "login" ? 'register' : "login");
    navigate(`/${toggleForm}`)
  };

  const validEmail = () => /.*@.*\.(.*){2,4}/.test(formData.email);

  const validatePassword = () => {
    const pass = formData.password;
    const errors = [];
    if (pass.length < 8) errors.push("At least 8 characters");
    if (pass.length > 50) errors.push("At most 50 characters");
    if (!/[a-z]/.test(pass)) errors.push("One lowercase letter");
    if (!/[A-Z]/.test(pass)) errors.push("One uppercase letter");
    if (!/\d/.test(pass)) errors.push("One number");
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(pass)) errors.push("One special character");
    return errors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validEmail()) return;
    const errors = validatePassword();
    if (errors.length) return errors;
  };

  return (
    <div
      fluid
      style={{
        display: "flex",
        padding: ".5rem",
        gap: "1rem",
        justifyContent: "space-between",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <CheckboxToggle onClick={handleChecked} checked={toggleForm === "register"} />

      <Form
        id={`${toggleForm}Form`}
        onSubmit={handleSubmit}
        style={{
          width: "100%",
          height: "100%",
          marginTop: "auto",
          marginBottom: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Row style={{ width: "100%", justifyContent: "center" }}>
          <Col xs={12} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <TextInput
              inputId="email"
              label={toggleForm}
              title="Email"
              placeholder="Email"
              onChange={handleChange}
            />

            {toggleForm === "register" && (
              <TextInput
                inputId="verification"
                title="Verify Email"
                placeholder="Re-enter email"
                disabled={formData.email.length === 0}
                onChange={handleChange}
              />
            )}

            <TextInput
              inputId="password"
              title="Password"
              placeholder="Password"
              info={
                toggleForm === "register"
                  ? ''
                  : ""
              }
              password={passHidden}
              onChange={handleChange}
            >
              <Button
                variant="link"
                onClick={() => setPassHidden(!passHidden)}
                style={{
                  fontSize: ".6rem",
                  lineHeight: "1rem",
                  padding: 0,
                  margin: 0,
                  textDecoration: "none",
                }}
              >
                {passHidden ? "show password" : "hide password"}
              </Button>
            </TextInput>

            {toggleForm === "register" && (
              <PasswordRequirements password={formData.password} />
            )}

            <Button
              type="submit"
              variant={toggleForm === "login" ? "primary" : "success"}
              disabled={
                formData.email === "" ||
                formData.password.length < 8 ||
                (toggleForm === "register" && formData.verification !== formData.email)
              }
              style={{
                alignSelf: "center",
                width: "50%",
                fontWeight: "bold",
                borderRadius: "0.5rem",
              }}
            >
              {toggleForm === "login" ? "Login" : "Register"}
            </Button>
          </Col>
        </Row>
      </Form>
    </div>
  );
}

export default LoginRegister;
