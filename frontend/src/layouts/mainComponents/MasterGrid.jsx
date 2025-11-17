import ProductCategories from '../layoutChildren/products/ProductCategories';
import FeaturedProducts from '../layoutChildren/products/FeaturedProducts';
import RecommendedProducts from '../layoutChildren/products/RecommendedProducts';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useTheme } from '@styles/themeContext';

function MasterGrid() {
  const { theme } = useTheme();

  return (
    <Row className="w-100 h-100 d-flex flex-row m-0 p-0 gap-2">
      <Col
        id="leftCol"
        className="flex-column m-0 p-0 h-100 d-none d-sm-flex flex-grow-0-ns"
        style={{ maxWidth: '20%', ...theme.schemes.highlight }}
      >
        <ProductCategories
          categories={['Really long category', 'Short Cat...', 3, 4]}
        />
      </Col>
      <Col
        id="rightCol"
        className="d-flex flex-column h-100 w-100 gap-2"
      >
        <Row
          id="featuredRow"
          className="d-flex flex-row"
          style={{ height: '55%', ...theme.schemes.highlight }}
        >
          <FeaturedProducts />
        </Row>
        <Row
          className="d-flex flex-row"
          style={{ height: '45%', ...theme.schemes.highlight }}
        >
          <RecommendedProducts />
        </Row>
      </Col>
    </Row>
  );
}

export default MasterGrid;
