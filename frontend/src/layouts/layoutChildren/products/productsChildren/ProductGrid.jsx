import Stack from 'react-bootstrap/Stack';

function ProductGrid({ children }) {
  return (
    <Stack
      direction='horizontal'
      className="d-flex flex-row flex-wrap h-100 w-100 m-0 p-1 gap-2"
      style={{ alignContent: 'flex-start' }}
    >
      {children}
    </Stack>
  );
}

export default ProductGrid;
