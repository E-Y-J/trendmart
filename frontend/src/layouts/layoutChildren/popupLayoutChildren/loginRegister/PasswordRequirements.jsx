import { ListGroup } from "react-bootstrap";

function PasswordRequirements({ password }) {
  const requirements = [
    { test: /.{8,50}/, text: "8–50 characters long" },
    { test: /[a-z]/, text: "At least one lowercase letter" },
    { test: /[A-Z]/, text: "At least one uppercase letter" },
    { test: /\d/, text: "At least one number" },
    { test: /[!@#$%^&*(),.?\\":{}|<>]/, text: "At least one special character (!@#$%^&*(),.?\":{}|<>)" },
  ];

  return (
    <ListGroup variant="flush" className="mt-1" style={{ fontSize: ".85rem" }}>
      {requirements.map((req, index) => {
        const passed = req.test.test(password);
        return (
          <ListGroup.Item
            key={index}
            style={{
              border: "none",
              padding: "0.25rem 0",
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
              color: passed ? "green" : "red",
            }}
          >
            {passed ? "✅" : "❌"}
            {req.text}
          </ListGroup.Item>
        );
      })}
    </ListGroup>
  );
}

export default PasswordRequirements;