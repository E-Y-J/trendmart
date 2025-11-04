import SearchbarHeader from "../sectionSearchbar/searchbarHeader";

function RecommendedProducts() {
  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        alignItems: 'center',
        gap: '0.5rem',
        backgroundColor: '#d9d9d9',
      }}
    >
    <SearchbarHeader searchId="recommendedSearch" placeholder="Recommended Products" sectionTitle="Recommended Products" />
    <h2 style={{color: "white"}}>Recommended Products Section</h2>
    </div>
  );
}

export default RecommendedProducts;