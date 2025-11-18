import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import { useTheme } from '@styles/themeContext';

function TextInput({
  children,
  inputId,
  placeholder,
  onChange,
  disabled = false,
  info = null,
  password = false,
}) {
  const { theme } = useTheme();

  return (
    <Form.Group
      style={{ width: '100%' }}
      controlId={inputId}
    >
      <InputGroup>
        <Form.Control
          type={password ? 'password' : 'text'}
          placeholder={placeholder}
          disabled={disabled}
          onChange={onChange}
          name={inputId}
          autoComplete="on"
          style={{
            color: theme.colors.contrast,
            backgroundColor: theme.colors.highlight,
            borderColor: theme.colors.splash,
          }}
        />
        {children}
      </InputGroup>
      {info && (
        <Form.Text
          style={{ padding: '.1rem 1rem 1rem 1rem', marginBottom: '1rem' }}
        >
          <em>{info}</em>
        </Form.Text>
      )}
    </Form.Group>
  );
}

export default TextInput;
