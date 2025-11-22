import { useEffect, useState, useCallback, useMemo } from 'react';
import Col from 'react-bootstrap/Col';
import ProductGrid from './productsChildren/ProductGrid';
import SearchbarRow from '../sectionSearchbar/SearchbarRow';
import ProductCard from './productsChildren/ProductCard';
import ProductPopup from './productsChildren/ProductPopup';
import { listProducts } from '@api/catalog';
import { normalizeProducts } from '../../../utils/normalizeProduct.js';

function FeaturedProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState(null);

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

  // Featured selection: take top 5 (by score if present, otherwise original order)
  const featured = useMemo(() => {
    if (!products.length) return [];
    const withScore = [...products].sort((a, b) => (b.score || 0) - (a.score || 0));
    return withScore.slice(0, 5);
  }, [products]);

  // When searching, search across all products; otherwise show featured subset
  const visible = useMemo(() => {
    if (search) {
      return products.filter(p =>
        (p.name && p.name.toLowerCase().includes(search)) ||
        (p.description && p.description.toLowerCase().includes(search))
      );
    }
    return featured;
  }, [products, featured, search]);

  // Placeholder handlers for future cart / buy integration
  const handleBuy = useCallback((p) => console.log('Buy', p.id), []);
  const handleAddToCart = useCallback((p) => console.log('Add to cart', p.id), []);
  const handleMoreLikeThis = useCallback((p) => console.log('More like', p.id), []);

  return (
    <Col className="d-flex flex-column w-100 p-0">
      <SearchbarRow
        searchId="featuredSearch"
        placeholder="Search Featured"
        sectionTitle="Featured Products"
        filterButton
        onSearch={handleSearch}
      />
      <ProductGrid>
        {loading && (<div className="text-muted">Loading...</div>)}
        {error && !loading && (<div className="text-danger">{error}</div>)}
        {!loading && !error && visible.map((p, idx) => (
          <div
            key={p.id || idx}
            style={{ flex: '0 0 180px', maxWidth: '180px', cursor: 'pointer' }}
            onClick={() => handleView(p)}
          >
            <ProductCard
              product={p}
              minimal
            />
          </div>
        ))}
      </ProductGrid>
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
