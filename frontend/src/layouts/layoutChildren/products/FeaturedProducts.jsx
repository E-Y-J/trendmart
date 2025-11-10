import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import ProductGrid from './productsChildren/productGrid';

import SearchbarRow from "../sectionSearchbar/SearchbarRow";

function FeaturedProducts() {
  return (
    <Col className='d-flex flex-column w-100 p-0 bg-danger' >
      <SearchbarRow
        searchId="featuredSearch"
        placeholder="Search Featured"
        sectionTitle="Featured Products"
        filterButton
        sm={ 6 }
      />
      <ProductGrid />
    </Col>
  );
}

export default FeaturedProducts;
