function ProductCategories({ categories }) {
  return (
    <div
      id="categoryContainer"
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        alignItems: 'center',
        gap: '0.5rem',
        backgroundColor: '#6c757d',
        borderRadius: '0.5rem',
      }}
    >
      {categories.map((category, index) => (
        <div
          key={index}
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            
            color: 'white',
            padding: '0.5rem', 
            margin: '0.25rem', 
            borderRadius: '0.375rem', 
            width: '75%',
            textAlign: 'center',
            fontWeight: 500,
            cursor: 'pointer',
            transition: 'transform 0.2s ease, background-color 0.2s ease',
          }}
        >
          <div
            style={{
              
              width: '100%',
              padding: '0.25rem',
              borderRadius: '0.25rem',
            }}
          >
            <h3 style={{ margin: 0 }}>{category}</h3>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ProductCategories;
