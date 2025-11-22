import ProductCategories from '../layoutChildren/products/ProductCategories';
import FeaturedProducts from '../layoutChildren/products/FeaturedProducts';
import RecommendedProducts from '../layoutChildren/products/RecommendedProducts';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useTheme } from '@resources/themes/themeContext';

function MasterGrid() {
  const { theme } = useTheme();

  return (
    <Row
      className="w-100 h-100 d-flex flex-row m-0"
      style={{ backgroundColor: theme.colors.whiteBg, padding: '2.5rem' }}
    >
      <Col
        id="leftCol"
        className="flex-column m-0 p-0 d-none d-sm-flex flex-grow-0-ns align-self-center"
        style={{
          maxWidth: '25%',
          height: '98%',
          borderRightStyle: 'solid',
          borderRightWidth: '.13rem',
          borderRightColor: theme.colors.details,
        }}
      >
        <ProductCategories
          categories={['Really long category', 'Short Cat...', 3, 4]}
        />
      </Col>

      <Col
        id="rightCol"
        className="d-flex flex-column h-100 w-100 ps-5"
        style={{ gap: '2.3rem' }}
      >
        <Row
          id="featuredRow"
          className="d-flex flex-row"
          style={{
            height: '55%',
            borderBottom: `.13rem solid ${theme.colors.details}`,
          }}
        >
          <FeaturedProducts />
        </Row>
        <Row
          className="d-flex flex-row"
          style={{ height: '45%' }}
        >
          <RecommendedProducts />
        </Row>
      </Col>
    </Row>
  );
}

export default MasterGrid;

// function MasterGrid() {
//   const { theme } = useTheme();

//   return (
//     <Row className="w-100 h-100 m-0 p-0 d-flex">
//       {/* LEFT SIDEBAR */}
//       <Col
//         id="leftCol"
//         className="d-none d-md-flex flex-column p-3"
//         style={{
//           maxWidth: '240px',
//           borderRight: '1px solid rgba(0,0,0,0.08)',
//           ...theme.schemes.highlight
//         }}
//       >
//         <ProductCategories
//           categories={[
//             'All',
//             'Nature',
//             'Travel',
//             'Food',
//             'Technology',
//             'Art'
//           ]}
//         />
//       </Col>

//       {/* RIGHT MAIN CONTENT */}
//       <Col className="d-flex flex-column px-3 gap-4">

//         {/* FEATURED SECTION */}
//         <div className="w-100">
//           <h4 className="mb-3">Featured Galleries</h4>
//           <div className="d-flex flex-row gap-3">
//             <FeaturedProducts />
//           </div>
//         </div>

//         {/* RECENT POSTS SECTION */}
//         <div className="w-100">
//           <h4 className="mb-3">Recent Posts</h4>
//           <div className="d-flex flex-row gap-3 mb-3">
//             <RecommendedProducts />
//           </div>

//           <div className="d-flex justify-content-end">
//             <button className="btn btn-primary">Load More</button>
//           </div>
//         </div>

//       </Col>
//     </Row>
//   );
// }
