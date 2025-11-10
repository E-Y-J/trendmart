import SearchbarHeader from "../sectionSearchbar/searchbarHeader";

function FeaturedProducts() {
  return (
    <div
      style={{
        width: '100%',
        height: '100%,'
      }}
    >
      <SearchbarHeader searchId="featuredSearch" placeholder="Featured Products" filterButton sectionTitle="Featured Products"/>
    </div>
  );
}

export default FeaturedProducts;