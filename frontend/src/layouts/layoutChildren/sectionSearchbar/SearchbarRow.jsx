import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Image from "react-bootstrap/Image";
import Row from "react-bootstrap/Row";
import filterIcon from "/filterIcon.svg?url";
import { useState, useCallback } from "react";

function SearchbarRow({
  searchId,
  placeholder,
  filterButton = false,
  sectionTitle = null,
  onSearch = null,
  debounceMs = 350,
  sm = null,
}) {
  const [value, setValue] = useState("");
  const [timer, setTimer] = useState(null);

  const handleChange = useCallback(
    (e) => {
      const next = e.target.value;
      setValue(next);
      if (onSearch) {
        if (timer) clearTimeout(timer);
        const t = setTimeout(() => onSearch(next), debounceMs);
        setTimer(t);
      }
      // eslint-disable-next-line react-hooks/exhaustive-deps
    },
    [onSearch, debounceMs, timer],
  );

  return (
    <Row
      id="featuredHeader"
      className="d-flex flex-grow-0 align-items-center m-0 w-100 px-1 py-0 px-sm-1 gap-1"
      style={{ height: "2.5rem", backgroundColor: "#9f9f9f" }}
    >
      <Col
        xs={10}
        sm={ sm }
        className="d-flex flex-grow-0 flex-shrink-1 align-items-center p-0"
      >
        <Form.Control
          id={ searchId }
          type="text"
          value={ value }
          placeholder={ placeholder }
          onChange={ handleChange }
          className="h-100 w-100"
          style={{ boxSizing: "border-box", fieldSizing: "content" }}
        />
      </Col>
      {filterButton && (
        <Col className="p-0" style={{ height: "2.5rem" }}>
          <Image
            alt="filter"
            src={ filterIcon }
            style={{ height: "100%", width: "auto", cursor: "pointer" }}
          />
        </Col>
      )}
      {sectionTitle && (
        <Col className="d-flex flex-grow-1 justify-content-end align-items-center text-light m-0 p-0 text-nowrap d-none d-sm-flex fs-4">
          { sectionTitle }
        </Col>
      )}
    </Row>
  );
}

export default SearchbarRow;
