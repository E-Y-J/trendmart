import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Button from "react-bootstrap/Button";

function FormSelectionToggle({ name }) {
  const FormCategory = ({ text }) => {
    const [isHovered, setIsHovered] = useState(false);

    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseOut = () => setIsHovered(false);

    const location = useLocation();
    const navigate = useNavigate();

    const currentForm = location.pathname.endsWith(`${text.toLowerCase()}`);

    const handleBackground = () => {
      if (isHovered) {
        return 'linear-gradient(.25turn, transparent, #fffffb, transparent)';
      } else if (currentForm) {
        return 'linear-gradient(.25turn, transparent 20%, #f3f3ea90 50%, transparent 80%)';
      } else {
        return '';
      }
    };

    return (
      <Button
        variant="light"
        onClick={() => navigate(`/${text.toLowerCase()}`)}
        onMouseEnter={handleMouseEnter}
        onMouseOut={handleMouseOut}
        style={{
          color: "#0a1f44",
          fontWeight: 700,
          transition: "all 0.3s ease",
          justifyContent: "center",
          margin: 0,
          width: "8rem",
          backgroundImage: handleBackground(),
          cursor: "pointer",
        }}
      >
        {text}
      </Button>
    );
  };

  return (
    <ButtonGroup
      id={name}
      style={{
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        position: "relative",
        borderRadius: ".4rem",
        fontSize: "1rem",
        height: "auto",
      }}
    >
      <FormCategory text="Login" />
      <FormCategory text="Register" />
    </ButtonGroup>
  );
}

export default FormSelectionToggle;
