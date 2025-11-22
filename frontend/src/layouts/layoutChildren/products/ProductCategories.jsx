import Col from "react-bootstrap/Col";
import Nav from "react-bootstrap/Nav";
import Spinner from "react-bootstrap/Spinner";
import { useCategoryCache } from "./productHooks/useCategoryCache";
import SearchbarRow from "../sectionSearchbar/SearchbarRow";
import { Row } from "react-bootstrap";

function ProductCategories() {
  // const { theme } = useTheme();
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
    <Col>
      <Row className="pe-4">
      <SearchbarRow searchId="category" placeholder="Categories" />
      </Row>
      <Nav className="flex-column p-3 bg-light h-100">

        {loading && <Spinner animation="border" size="sm" />}

        {error && <div className="text-danger">Failed to load categories.</div>}

        {!loading && !error && categories?.length > 0 && (
          <>
            {categories.map(cat => (
              <Nav.Link key={cat.id} href={`/category/${cat.slug}`}>
                {cat.name}
              </Nav.Link>
            ))}
          </>
        )}
      </Nav>
    </Col>
  );
}

export default ProductCategories;
