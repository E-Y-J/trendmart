

function TextInput({ children, inputId, title, placeholder, onChange, disabled=false, info=null, password=false }) {
  return (
    <div
      style={{
        width: '100%'
      }}
    >
      <label
        name={ inputId }
        htmlFor={ inputId }
        style={{
          display: 'flex',
          flexDirection: 'row',
          padding: '.3rem .3rem .3rem 1rem',
          gap: '.5rem',
          border: '2px solid #0a1f44',
          whiteSpace: 'nowrap',
          color: '#fffffb',
          backgroundColor: '#0a1f44',
          borderRadius: '1rem .4rem .4rem 1rem'
        }}
      >
        { title }
      <input
        id={ inputId }
        name={ inputId }
        type={ password ? 'password' : 'text'}
        placeholder={ placeholder }
        disabled={ disabled }
        onChange={ onChange }
        autoComplete="on"
        style={{
          width: '100%',
          border: 'none',
          justifyContent: 'center',
          boxSizing: 'border-box',
          fieldSizing: 'content',
        }}
      />
        {children}
      </label>
      { info &&
        <div
          style={{
            fontSize: '.8rem',
            padding: '.1rem 1rem 1rem 1rem',
            marginBottom: '1rem'
          }}
        >
          <em>
            { info }
          </em>
        </div>
      }
    </div>
  )
}

export default TextInput;