import filterIcon from '/filterIcon.svg?url'

function SearchbarHeader({ searchId, placeholder, filterButton=false, sectionTitle=null }) {
  return (
    <div
      id='featuredHeader'
      style={{
        height: '2.5rem',
        width: '100%',
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        padding: '.5rem',
        backgroundColor: '#9f9f9f',
      }}
    >
      {/* Search Input Group */}
      <div
        style={{
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          gap: '.5rem'
        }}
      >
        <input
          id={ searchId }
          type='text'
          placeholder={ placeholder }
          style={{
            height: '100%',
            width: '100%',
            boxSizing: 'border-box',
          }}
        />
        
        { filterButton && <input alt="filter" type="image" src={ filterIcon } style={{ height: '100%', width: 'auto' }} /> }
      </div>
      
      {/* Title */}
      <div
        style={{
          flex: 1,
          color: 'fffffb',
          display: 'flex',
          justifyContent: 'flex-end',
        }}
      >
        { sectionTitle && <h1 style={{ margin: 0, fontSize: '1.5rem' }}>{ sectionTitle }</h1> }
      </div>
    </div>
  )
}

export default SearchbarHeader;
