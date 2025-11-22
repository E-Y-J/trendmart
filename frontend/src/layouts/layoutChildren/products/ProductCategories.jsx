import { useState, useEffect } from 'react';
import Stack from 'react-bootstrap/Stack';
import SearchbarRow from '../sectionSearchbar/SearchbarRow';
import { Container } from 'react-bootstrap';
import { listCategories } from '@api/catalog';
import HoverCategory from './productsChildren/HoverCategory';

function ProductCategories() {
  const [categories, setCategories] = useState(null); // null = loading

  useEffect(() => {
    async function fetchData() {
      const result = await listCategories();
      setCategories(result);
    }
    fetchData();
  }, []);

  // Placeholder mode
  const placeholderCategories = [
    { id: 'ph-1', name: 'Category 1', slug: 'category-1' },
    { id: 'ph-2', name: 'Category 2', slug: 'category-2' },
    { id: 'ph-3', name: 'Category 3', slug: 'category-3' },
    { id: 'ph-4', name: 'Category 4', slug: 'category-4' },
  ];

  const displayedCategories = categories?.length ? categories : placeholderCategories;

  return (
    <Container
      fluid
      className="p-0 m-0"
      style={{ height: '100%' }}
    >
      <Stack
        direction="vertical"
        className="d-flex justify-content-start align-items-center gap-2 m-0 p-0 w-100"
      >
        <div className='d-flex flex-column ms-3 justify-content-center align-items-center align-self-start'>
          <SearchbarRow searchId="subcategorySearch" placeholder="Category" />
        </div>

        {displayedCategories.map((cat) => (
          <HoverCategory key={cat.id} linksTo={`/catalog/${cat.slug}`}>
            {cat.name}
          </HoverCategory>
        ))}
      </Stack>
    </Container>
  );
}

export default ProductCategories;

