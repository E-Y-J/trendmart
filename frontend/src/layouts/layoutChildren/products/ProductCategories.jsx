import Stack from 'react-bootstrap/Stack';
import SearchbarRow from '../sectionSearchbar/SearchbarRow';
import { Container } from 'react-bootstrap';
import { useTheme } from '@styles/themeContext';

function ProductCategories({ categories }) {
  const { theme } = useTheme();

  return (
    <Container
      fluid
      className="p-0 m-0"
      style={{ height: '100%' }}
    >
      <Stack
        direction="vertical"
        className="gap-2"
      >
        <SearchbarRow
          searchId="subcategorySearch"
          placeholder="Category"
          sm={12}
        />
        {categories.map((category, index) => (
          <h3
            key={index}
            className="m-0"
            style={{ ...theme.buttons.splash }}
          >
            {category}
          </h3>
        ))}
      </Stack>
    </Container>
  );
}

export default ProductCategories;
