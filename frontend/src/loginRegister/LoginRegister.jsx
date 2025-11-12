import { useState } from "react";
import TextInput from "../layouts/layoutChildren/input/TextInput";
import CheckboxToggle from "../layouts/layoutChildren/input/CheckboxToggle";
import { useNavigate } from "react-router-dom";
import api from "../api/api"
// import { createUser, loginUser } from "../redux/auth/authSlice";


function LoginRegister({ formName }) {
  const [formData, setFormData] = useState({ email: '', password: '', verification: '' })
  const [passHidden, setPassHidden] = useState(true)
  const [errors, setErrors] = useState([])
  const navigate = useNavigate()

  const handleChange = (event) => {
    const { id, value } = event.target
    setFormData((prev) => ({
      ...prev,
      [id]: value
    }))
  }

  const handleChecked = () => {
    formName == 'login' ? navigate('/register') : navigate('/login')
  }

  const validEmail = () => /.*@.*\.(.*){2,4}/.test(formData.email)

  // must satisfy length requirements first
  // regular expression mirrors backend
  const validatePassword = () => {
    const passLength = formData.password.length
    const pass = formData.password
    const errors = [];
    if (passLength < 8) errors.push("At least 8 characters");
    if (passLength > 50) errors.push("At most 50 characters")
    if (!/[a-z]/.test(pass)) errors.push("One lowercase letter");
    if (!/[A-Z]/.test(pass)) errors.push("One uppercase letter");
    if (!/[\d]/.test(pass)) errors.push("One number");
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(pass)) errors.push("One special character");
    return errors;
  }

  const handleSubmit = async () => {
    // collect client-side validation errors
    let clientErrors = validatePassword();
    if (!validEmail()) clientErrors = ["Email doesn't match required format.", ...clientErrors];
    if (formName === 'register' && formData.verification !== formData.email) {
      clientErrors = ["Emails do not match.", ...clientErrors];
    }
    if (clientErrors.length) {
      setErrors(clientErrors);
      return; // stop submit
    }

    const authData = { email: formData.email.trim(), password: formData.password };
    try {
      const response = await api.post(`/auth/${formName}`, authData);
      console.log('Auth success:', response.data);
      setErrors([]);
      return response.data;
    } catch (error) {
      // surface backend validation (marshmallow) or duplicate email errors
      if (error.response) {
        const payload = error.response.data;
        let serverErrors = [];
        if (Array.isArray(payload)) serverErrors = payload;
        else if (typeof payload === 'string') serverErrors = [payload];
        else if (payload && typeof payload === 'object') {
          serverErrors = Object.entries(payload).flatMap(([field, msgs]) => Array.isArray(msgs) ? msgs.map(m => `${field}: ${m}`) : [`${field}: ${msgs}`]);
        }
        setErrors(serverErrors.length ? serverErrors : ['Registration failed.']);
        console.error('Auth failed:', error.response.status, payload);
      } else {
        setErrors([error.message]);
        console.error('Network error:', error.message);
      }
    }
  }

  return (
    <div
      style={{
        width: '23rem',
        height: '20rem',
        display: 'flex',
        padding: '.5rem',
        gap: '1rem',
        justifyContent: 'space-between',
        alignContent: 'center',
        flexDirection: 'column',
      }}
    >
      <CheckboxToggle name="logRegToggle" onClick={handleChecked} checked={formName == 'register'} />

      <form
        onSubmit={e => {
          e.preventDefault();
          handleSubmit();
        }}
        id={`${formName}Form`}
        style={{
          height: '100%',
          flexDirection: 'row',
          gap: 'inherit',
          marginTop: 'auto',
          marginBottom: 'auto'
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'inherit',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          {errors.length > 0 && (
            <ul style={{ color: 'red', fontSize: '.65rem', margin: 0, padding: 0, listStyle: 'none', textAlign: 'left', maxWidth: '100%' }}>
              {errors.map((err, i) => <li key={i}>{err}</li>)}
            </ul>
          )}
          <TextInput
            inputId="email"
            label={formName}
            title="Email"
            placeholder="e.g. user@email.com"
            onChange={handleChange}
          />
          {formName == 'register' &&
            <TextInput
              inputId="verification"
              title="Verify Email"
              placeholder="Re-enter email"
              // disable verification email if email isn't filled out
              disabled={formData.email.length == 0}
              onChange={handleChange}
            />
          }
          <TextInput
            inputId="password"
            title="Password"
            placeholder="Enter your password"
            info={formName == 'register' ? 'Passwords must be 8-50 characters long and include at least one of each following characters are required: lowercase, uppercase, number, and !@#$%^&*(),.?":{}|<></>' : ''}
            password={passHidden}
            onChange={handleChange}
          >
            <button id="showbutton" type="button" onClick={() => setPassHidden(!passHidden)} style={{ fontSize: '.4rem' }}>
              show
              <br />
              password
            </button>
          </TextInput>
          <button
            type="submit"
            disabled={
              formData.email == '' ||
              formData.password.length < 8 ||
              formName == 'register' && formData.verification != formData.email
            }
            style={{
              flexDirection: 'row',
              maxWidth: '50%',
              alignContent: 'flex-end'
            }}
          >
            {formName === 'login' ? 'Login' : 'Register'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default LoginRegister;