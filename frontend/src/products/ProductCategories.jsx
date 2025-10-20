import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Stack from "react-bootstrap/Stack";
import Badge from "react-bootstrap/Badge";

function ProductCategories({ categories }) {
  return (
    <Stack direction="column" className="w-100 h-100 d-flex justify-content-start align-items-center gap-2 my-2">
      { categories.map((category, index) => (
        <Badge pill key={index} className="text-white bg-tertiary p-2 m-1 rounded-2 w-75 text-center">
          <div className="bg-primary">
            <h3>
              {category}
            </h3>
          </div>
        </Badge>
      ))}
    </Stack>
  )
};

export default ProductCategories;