import ProductCategories from '../layoutChildren/products/ProductCategories';
import FeaturedProducts from '../layoutChildren/products/FeaturedProducts';
import RecommendedProducts from '../layoutChildren/products/RecommendedProducts';

function MasterGrid() {
  return (
    <div style={{ width: '98%', alignContent: 'center', marginLeft: 'auto', marginRight: 'auto' }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          width: '100%',
          margin: 0,
          padding: 0,
          minHeight: '75vh',
        }}
      >
        {/* Category Column */}
        <div
          id="category"
          style={{
            flexBasis: '14.666%', 
            display: 'flex',
            justifyContent: 'space-evenly',
            flexDirection: 'column',
            gap: '0.5rem',
            margin: 0,
            padding: 0,
          }}
        >
          <ProductCategories categories={[1, 2, 3, 4]} />
        </div>

        {/* Products Column */}
        <div
          id="products"
          style={{
            flexBasis: '82.333%',
            display: 'flex',
            flexDirection: 'column',
            gap: '2%',
            margin: 0,
            padding: 0,
          }}
        >
          {/* Header Row */}
          <div
            style={{
              display: 'flex',
              margin: 0,
              padding: 0,
              justifyContent: 'center',
              alignItems: 'center',
              width: '100%',
            }}
          >
            <div
              style={{
                flexBasis: '33.333%',
                margin: '0 0.5rem',
                padding: 0,
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                backgroundColor: '#2d2d2d',
              }}
            >
              SearchBar
            </div>
            <div
              style={{
                flex: 1,
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                paddingRight: '1rem',
              }}
            >
              <h1 style={{ margin: 0 }}>Current Category Title</h1>
            </div>
          </div>

          {/* Featured Products Row */}
          <div
            id="featured"
            style={{
              margin: 0,
              padding: 0,
              height: '60%',
              width: '100%',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <FeaturedProducts />
          </div>

          {/* Recommended Products Row */}
          <div
            id="recommended"
            style={{
              margin: 0,
              padding: 0,
              height: '40%',
              width: '100%',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <RecommendedProducts />
          </div>
        </div>
      </div>
    </div>
  );
}

export default MasterGrid;
