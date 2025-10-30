import ProductCategories from '../layoutChildren/products/ProductCategories';
import FeaturedProducts from '../layoutChildren/products/FeaturedProducts';
import RecommendedProducts from '../layoutChildren/products/RecommendedProducts';

function MasterGrid() {
  return (
      <>
        {/* Category Column */}
        <div
          id="category"
          style={{
            flexBasis: '10%', 
            display: 'flex',
            justifyContent: 'space-evenly',
            flexDirection: 'column',
            margin: 0,
            padding: 0,
          }}
        >
          <ProductCategories categories={['Something really long', 2, 3, 4]} />
        </div>

        {/* Products Column */}
        <div
          id="products"
          style={{
            flexBasis: '89%',
            display: 'flex',
            flexDirection: 'column',
            gap: '2%',
            margin: 0,
            padding: 0,
          }}
        >

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
            {/* Header Row */}
            <div
              style={{
                width: '100%',
                height: '100%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                backgroundColor: '#9f9f9f',
                borderRadius: '0.5rem',
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
      </>
  );
}

export default MasterGrid;
