import Stack from 'react-bootstrap/Stack';
import SearchbarRow from "../sectionSearchbar/SearchbarRow";
import { Container } from 'react-bootstrap';

function ProductCategories({ categories }) {
  return (
    <Container fluid className='p-0 m-0' style={{ height: '100%' }}>
      <Stack direction='vertical' className='gap-2'>
        <SearchbarRow searchId="subcategorySearch" placeholder="Category" />
        {categories.map((category, index) => (
          <h3 key={index} className="bg-white" style={{ margin: 0 }}>{category}</h3>
        ))}
      </Stack>
    </Container>
  );
}

export default ProductCategories;
