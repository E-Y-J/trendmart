import ProductCategories from '../layoutChildren/products/ProductCategories';
import FeaturedProducts from '../layoutChildren/products/FeaturedProducts';
import RecommendedProducts from '../layoutChildren/products/RecommendedProducts';

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
        {/* Header Row (Search and Title) - This itself should be a row */}
          <div
            id='featuredHeader'
            style={{
              height: '6%',
              display: 'flex',
              flexDirection: 'row', // Display search and title side-by-side
              alignItems: 'center',
              padding: '.5rem',
              backgroundColor: '#9f9f9f',
            }}
          >
            {/* Search Input Group */}
            <div style={{ marginLeft: '1%', display: 'flex', alignItems: 'center', gap: '.5rem' }}>
              <input
                id='categorySearch'
                type='text'
                placeholder='Search Subcategory'
              />
            </div>
          </div>
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
          {/* Header Row (Search and Title) - This itself should be a row */}
          <div
            id='featuredHeader'
            style={{
              height: '10%',
              display: 'flex',
              flexDirection: 'row', // Display search and title side-by-side
              alignItems: 'center',
              padding: '.5rem',
              backgroundColor: '#9f9f9f',
            }}
          >
            {/* Search Input Group */}
            <div style={{ marginLeft: '1%', display: 'flex', alignItems: 'center', gap: '.5rem' }}>
              <input
                id='featureSearch'
                type='text'
                placeholder='Search Featured Products'
              />
            </div>
            
            {/* Title */}
            <div
              style={{
                flex: 1, // Pushes the title to the right
                color: 'white',
                display: 'flex',
                justifyContent: 'flex-end', // Aligns title to the right
                paddingRight: '1rem',
                
              }}
            >
              <h1 style={{ margin: 0, fontSize: '1.5rem' }}>Current Category Title</h1>
            </div>
          </div>
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
          {/* Header Row (Search and Title) - This itself should be a row */}
          <div
            id='featuredHeader'
            style={{
              height: '15%',
              display: 'flex',
              flexDirection: 'row', // Display search and title side-by-side
              alignItems: 'center',
              padding: '.5rem',
              backgroundColor: '#9f9f9f',
            }}
          >
            {/* Search Input Group */}
            <div style={{ marginLeft: '1%', display: 'flex', alignItems: 'center', gap: '.5rem' }}>
              <input
                id='recommendedSearch'
                type='text'
                placeholder='Search Recommended Products'
              />
            </div>
            
            {/* Title */}
            <div
              style={{
                flex: 1, // Pushes the title to the right
                color: 'white',
                display: 'flex',
                justifyContent: 'flex-end', // Aligns title to the right
                paddingRight: '1rem',
                
              }}
            >
              <h1 style={{ margin: 0, fontSize: '1.5rem' }}>Highest Scoring Recommendations</h1>
            </div>
          </div>
          <RecommendedProducts />
        </div>
      </div>
    </div>
  );
}

export default MasterGrid;