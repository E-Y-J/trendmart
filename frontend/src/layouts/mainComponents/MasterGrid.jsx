import ProductCategories from '../layoutChildren/products/ProductCategories';
import FeaturedProducts from '../layoutChildren/products/FeaturedProducts';
import RecommendedProducts from '../layoutChildren/products/RecommendedProducts';
import SearchbarHeader from '../layoutChildren/sectionSearchbar/SearchbarHeader';

function MasterGrid() {
  return (
    // 1. PRIMARY CONTAINER: Display Flex (Row) to hold two main columns side-by-side
    <div
      style={{
        display: 'flex',
        flexDirection: 'row', // Horizontal arrangement (Category | Products)
        flex: 1, // Allow the MasterGrid to fill the space in the MasterLayout
        gap: '.5rem', // Added padding for overall spacing
      }}
    >

      {/* 2. CATEGORY COLUMN: Fixed width, occupies the left side */}
      <div
        id="category"
        style={{
          width: '15%', // Set a visible width (e.g., 20%)
          display: 'flex',
          justifyContent: 'flex-start', // Align categories to the top
          flexDirection: 'column',
          // Adjust min-width if categories are very long
        }}
      >
        <ProductCategories categories={['Really long category', 'Short Category', 3, 4]} />
      </div>

      {/* 3. PRODUCTS COLUMN: Takes up the remaining width and uses FLEX DIRECTION COLUMN to stack the two rows */}
      <div
        id="products"
        style={{
          flex: 1, // Takes up the rest of the available space (80%)
          display: 'flex',
          flexDirection: 'column', // Vertical arrangement (Featured then Recommended)
          gap: '.5rem', // Gap between Featured and Recommended sections
          margin: 0,
          padding: 0,
        }}
      >

        {/* 4. FEATURED PRODUCTS ROW (Header and Content) */}
        <div
          id="featuredContainer"
          style={{
            height: '60%', // Adjust height proportion as needed
            display: 'flex',
            flexDirection: 'column', // Now that this is the content, use column/row layout as needed
            gap: '.5rem',
            backgroundColor: '#717171'
          }}
        >
          {/* Pass search header above featured products for future semantic search integration */}
          <SearchbarHeader searchId="featuredSearch" placeholder="Search products..." sectionTitle="Featured" />
          <FeaturedProducts />
        </div>

        {/* 5. RECOMMENDED PRODUCTS ROW */}
        <div
          id="recommended"
          style={{
            height: '40%',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <SearchbarHeader searchId="recommendedSearch" placeholder="Refine recommendations..." sectionTitle="Recommended" />
          <RecommendedProducts />
        </div>
      </div>
    </div>
  );
}

export default MasterGrid;