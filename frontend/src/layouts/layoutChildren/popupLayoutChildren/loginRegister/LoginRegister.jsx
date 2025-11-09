import { useState, useEffect } from "react";
import { Form, Button, Row, Col } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { loginUser, createUser } from "../../../../redux/auth/authSlice";
import { setStatus, clearStatus } from "../../../../redux/status/statusSlice"
import TextInput from "../../input/TextInput";
import CheckboxToggle from "../../input/CheckboxToggle";
import PasswordRequirements from "./PasswordRequirements";

function LoginRegister() {
  const [formData, setFormData] = useState({ email: "", password: "", verification: "" });
  const [toggleForm, setToggleForm] = useState("login");
  const [passHidden, setPassHidden] = useState(true);
  const navigate = useNavigate()
  const dispatch = useDispatch()


  const handleChange = (event) => {
    const { id, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  useEffect(() => {
    navigate(`/${ toggleForm }`)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [toggleForm])

  const handleChecked = () => {
    setToggleForm(toggleForm === "login" ? 'register' : "login");
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

  const handleSubmit = async(e) => {
    // prevent default or url path will change unnecessarily
    e.preventDefault();
    // dismiss previous alert if any
    dispatch(clearStatus());
    // validate email
    if (!validEmail()) {
      dispatch(setStatus({ message: "Invalid email format.", variant: "error"}))
      return;
    }
    // return password criteria errors
    const errors = validatePassword();
    if (errors.length) {
      dispatch(setStatus({ message: `Unmet password criteria: ${errors.join(", ")}.` }))
      return;
    }
    // take email and password from formData
    const authData = { email: formData.email, password: formData.password }
      if (toggleForm === 'login') {
        const result = await dispatch(loginUser(authData)).unwrap();
        console.log('Login successful:', result);
      } else {
        const result = await dispatch(createUser(authData)).unwrap();
        console.log('Registration successful:', result);
      }
    };
    

  return (
    <div
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
        className="h-100 w-100 d-flex flex-column gap-1 justify-content-center align-items-center my-auto"
        onSubmit={ handleSubmit }
      >
        <Row style={{ width: "100%", justifyContent: "center" }}>
          <Col className="d-flex flex-column gap-1" style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <TextInput
              inputId="email"
              label={ toggleForm }
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
                onChange={ handleChange }
              />
            )}

            <TextInput
              inputId="password"
              title="Password"
              label={ toggleForm }
              placeholder="Password"
              info={
                toggleForm === "register"
                  ? ''
                  : ""
              }
              password={passHidden}
              onChange={ handleChange }
            >
              <Button
                variant="danger"
                onClick={() => setPassHidden(!passHidden)}
                style={{
                  fontSize: ".6rem",
                  lineHeight: "1rem",
                  padding: 0,
                  margin: 0,
                  textDecoration: "none",
                }}
              >
                {passHidden ? "show" : "hide"}
                <br />
                password
              </Button>
            </TextInput>

            {toggleForm === "register" && (
              <PasswordRequirements password={ formData.password } />
            )}

            <Button
              type="submit"
              className="w-50 align-self-center fw-bold border-1"
              style={{
                borderRadius: "0.5rem",
                backgroundColor: toggleForm === "login" ? "#0a1f44" : "#00aef0"
              }}
              disabled={
                formData.email === "" ||
                formData.password.length < 8 ||
                (toggleForm === "register" && formData.verification !== formData.email)
              }
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
