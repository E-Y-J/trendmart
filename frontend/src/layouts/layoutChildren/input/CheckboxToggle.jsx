function CheckboxToggle({ onClick, checked }) {
  return (
    <div
      id="toggleContainer"
      style={{
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        position: "relative",
        borderRadius: ".4rem",
        backgroundImage: "linear-gradient(to bottom, #f3f3ea, #f0f0f0)",
        boxShadow: "0 1px 1px rgb(255 255 255 / .6)",
        fontSize: "1rem",
        height: 'auto'
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
      <input
        type="checkbox"
        checked={checked}
        onChange={ onClick }
        style={{
          appearance: "none",
          position: "absolute",
          zIndex: 1,
          borderRadius: "inherit",
          width: "100%",
          height: "100%",
          font: "inherit",
          opacity: 0,
          cursor: "pointer",
        }}
      />
      <div
        id="buttonContainer"
        style={{
          display: "flex",
          alignItems: "center",
          position: "relative",
          borderRadius: ".375rem",
          width: "3rem",
          height: "1.5rem",
          backgroundColor: checked ? "#00aef0" : "#0a1f44",
          boxShadow:
            "inset 0 0 .0625rem .125rem rgb(255 255 255 / .2), inset 0 .0625rem .125rem rgb(0 0 0 / .4)",
          transition: "background-color .4s linear",
        }}
      >
        <div
          id="toggleButton"
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            position: "absolute",
            left: checked ? "1.5625rem" : ".0625rem",
            borderRadius: ".3125rem",
            width: "1.375rem",
            height: "1.375rem",
            backgroundColor: "#3ba9ff",
            boxShadow:
              "inset 0 -.0625rem .0625rem .125rem rgb(0 0 0 / .1), inset 0 -.125rem .0625rem rgb(0 0 0 / .2), inset 0 .1875rem .0625rem rgb(255 255 255 / .3), 0 .125rem .125rem rgb(0 0 0 / .5)",
            transition: "left .4s",
          }}
        >
        </div>
      </div>
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
    </div>
  )
}

export default CheckboxToggle