import { useEffect, useState, useCallback, useMemo } from 'react';
import Button from 'react-bootstrap/Button'
import Col from 'react-bootstrap/Col';
import ProductGrid from './productsChildren/ProductGrid';
import SearchbarRow from '../sectionSearchbar/SearchbarRow';
import ProductPopup from './productsChildren/ProductPopup';
import { listProducts } from '@api/catalog';
import { normalizeProducts } from '@utils/helpers';
import { useTheme } from '@resources/themes/themeContext';

function FeaturedProducts() {
  const { theme } = useTheme();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState(null);
  const [pageIndex, setPageIndex] = useState(0); // carousel page
  const pageSize = 4;

  useEffect(() => {
    let ignore = false;
    async function run() {
      setLoading(true);
      setError(null);
      try {
        const raw = await listProducts();
        if (!ignore) setProducts(normalizeProducts(raw));
      } catch (e) {
        if (!ignore) setError(e.message || 'Failed to load products');
      } finally {
        if (!ignore) setLoading(false);
      }
    }
    run();
    return () => { ignore = true; };
  }, []);

  const handleSearch = useCallback((value) => setSearch(value.trim().toLowerCase()), []);
  const handleView = useCallback((p) => setSelected(p), []);
  const handleClosePopup = useCallback(() => setSelected(null), []);

  // Featured selection: take top 10 (by score if present, otherwise original order)
  const featured = useMemo(() => {
    if (!products.length) return [];
    const withScore = [...products].sort((a, b) => (b.score || 0) - (a.score || 0));
    return withScore.slice(0, 10);
  }, [products]);

  // When searching, search across all products
  const searchResults = useMemo(() => {
    if (!search) return [];
    return products.filter(p =>
      (p.name && p.name.toLowerCase().includes(search)) ||
      (p.description && p.description.toLowerCase().includes(search))
    );
  }, [products, search]);

  // Active filtered set (search overrides featured)
  const filteredProducts = useMemo(() => (search ? searchResults : featured), [search, searchResults, featured]);

  // Pagination metrics
  const totalProducts = filteredProducts.length;
  const totalPages = Math.max(1, Math.ceil(totalProducts / pageSize));
  const start = pageIndex * pageSize;
  const end = start + pageSize;
  const visibleProducts = filteredProducts.slice(start, end);

  // Clamp / reset page index when data set changes
  useEffect(() => {
    setPageIndex(prev => Math.min(prev, totalPages - 1));
  }, [totalPages]);
  useEffect(() => {
    // Reset to first page on new search term for better UX
    setPageIndex(0);
  }, [search]);

  // Placeholder handlers for future cart / buy integration
  const handleBuy = useCallback((p) => console.log('Buy', p.id), []);
  const handleAddToCart = useCallback((p) => console.log('Add to cart', p.id), []);
  const handleMoreLikeThis = useCallback((p) => console.log('More like', p.id), []);

  const handlePrevPage = useCallback(() => {
    setPageIndex(prev => Math.max(0, prev - 1));
  }, []);
  const handleNextPage = useCallback(() => {
    setPageIndex(prev => Math.min(totalPages - 1, prev + 1));
  }, [totalPages]);

  return (
    <Col className="d-flex flex-column w-100 p-0">
      <SearchbarRow
        searchId="featuredSearch"
        placeholder="Search Featured"
        sectionTitle="Featured Products"
        filterButton
        onSearch={handleSearch}
      />

      <div className="d-flex flex-column w-100">
        <div className="d-flex justify-content-between align-items-center mb-2 px-1">
          <Button
            type="button"
            onClick={handlePrevPage}
            disabled={pageIndex === 0}
            className="btn btn-sm"
            style={{
              ...theme.buttons.emphasis
            }}
          >
            Prev
          </Button>
          <span className="small">
            Page {totalProducts === 0 ? 0 : pageIndex + 1} of {totalPages}
          </span>
          <Button
            type="button"
            onClick={handleNextPage}
            disabled={pageIndex >= totalPages - 1}
            className="btn btn-sm"
            style={{
              ...theme.buttons.emphasis
            }}
          >
            Next
          </Button>
        </div>

        <ProductGrid
          products={visibleProducts}
          onSelect={setSelected}
          onAddToCart={handleAddToCart}
          loading={loading}
          error={error}
        />
      </div>

      <ProductPopup
        product={selected}
        show={!!selected}
        onClose={handleClosePopup}
        onAddToCart={handleAddToCart}
        onBuyNow={handleBuy}
        onMoreLikeThis={handleMoreLikeThis}
      />
    </Col>
  );
}

export default FeaturedProducts;
