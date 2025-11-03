import {  useState } from "react";
import TextInput from "../layouts/layoutChildren/input/textInput";
import CheckboxToggle from "../layouts/layoutChildren/input/CheckboxToggle";


function LoginRegister() {
  const [formData, setFormData]  = useState({ email: '', password: '', verification: '' })
  const [toggleForm, setToggleForm] = useState('login')
  const [passHidden, setPassHidden] = useState(true)

  const handleChange = (event) => {
    const { id, value } = event.target
    setFormData((prev) => ({
      ...prev,
      [id]: value
    }))
  }

  const handleChecked = () => {
    toggleForm == 'login' ? setToggleForm('register') : setToggleForm('login')
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
      if (/[^a-z]/.test(pass)) errors.push("One lowercase letter");
    if (/[^A-Z]/.test(pass)) errors.push("One uppercase letter");
    if (/[^\d]/.test(pass)) errors.push("One number");
    if (/[^!@#$%^&*(),.?":{}|<>]/.test(pass)) errors.push("One special character");
    return errors;
  }

  const handleSubmit = () => {
    if (!validEmail()) return

    const errors = validatePassword()
    if (errors.length) return errors

    
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
      <CheckboxToggle onClick={ handleChecked } checked={ toggleForm == 'register' } />
      
      <form
        id={ `${toggleForm}Form` }
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
          <TextInput
            inputId="email"
            label={ toggleForm }
            title="Email"
            placeholder="e.g. user@email.com"
            onChange={ handleChange }
          />
          { toggleForm == 'register' &&
            <TextInput
              inputId="verification" 
              title="Verify Email"
              placeholder="Re-enter email"
              // disable verification email if email isn't filled out
              disabled={ formData.email.length == 0 }
              onChange={ handleChange }
            />
          }
          <TextInput
            inputId="password"
            title="Password"
            placeholder="Enter your password"
            info={ toggleForm == 'register' ? 'Passwords must be 8-50 characters long and include at least one of each following characters are required: lowercase, uppercase, number, and !@#$%^&*(),.?":{}|<></>' : '' }
            password={ passHidden }
            onChange={ handleChange }
          >
            <button id="showbutton" onClick={ () => setPassHidden(!passHidden) } style={{fontSize: '.4rem'}}>
              show
              <br/>
              password
            </button>
          </TextInput>
          <button
            type="submit"
            onSubmit={ handleSubmit }
            disabled={
              formData.email == '' ||
              formData.password.length < 8 ||
              toggleForm == 'register' && formData.verification != formData.email
            }
            style={{
              flexDirection: 'row',
              maxWidth: '50%',
              alignContent: 'flex-end'
            }}
          >
            { toggleForm === 'login' ? 'Login' : 'Register' }
          </button>
        </div>
      </form>
    </div>
  )
}

export default LoginRegister;