import { useEffect, useState, useCallback } from 'react';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import SearchbarRow from '../sectionSearchbar/SearchbarRow';
import {
  getColdStart,
  searchRecommendations,
  getSimilarById,
} from '@api/recommendations';
import {
  logView,
  logCartAdd,
  sendRecommendationFeedback,
} from '@api/events';
import PopupLayout from '@main/PopupLayout';
import { useTheme } from '@styles/themeContext';
import { Button } from 'react-bootstrap';

function RecommendedProducts() {
  const { theme } = useTheme();
  const [state, setState] = useState({ loading: true, error: null, items: [] });
  const [searchState, setSearchState] = useState({
    query: '',
    loading: false,
    error: null,
    items: [],
  });
  const searching = searchState.query.length > 0;
  const [similarState, setSimilarState] = useState({
    open: false,
    base: null,
    loading: false,
    error: null,
    items: [],
  });

  const performSearch = useCallback(async (q) => {
    setSearchState((s) => ({ ...s, query: q }));
    if (!q) {
      setSearchState({ query: '', loading: false, error: null, items: [] });
      return;
    }
    setSearchState((s) => ({ ...s, loading: true, error: null }));
    try {
      const data = await searchRecommendations(q, 12);
      const items = Array.isArray(data?.results) ? data.results : [];
      setSearchState({ query: q, loading: false, error: null, items });
    } catch (err) {
      setSearchState({
        query: q,
        loading: false,
        error: err?.message || 'Search failed',
        items: [],
      });
    }
  }, []);

  useEffect(() => {
    let isActive = true;
    (async () => {
      try {
        const data = await getColdStart(8);
        const items = Array.isArray(data?.results) ? data.results : [];
        if (isActive) setState({ loading: false, error: null, items });
      } catch (err) {
        if (isActive)
          setState({
            loading: false,
            error: err?.message || 'Failed to load',
            items: [],
          });
      }
    })();
    return () => {
      isActive = false;
    };
  }, []);

  return (
    <Col
      className="d-flex flex-column justify-content-start align-items-center m-0 p-0"
      style={{ width: '100%', height: '100%' }}
    >
      <SearchbarRow
        searchId="recommendedSearch"
        placeholder="Search recommended products"
        sectionTitle="Recommended Products"
        onSearch={performSearch}
        sm={6}
      />
      <Row className="m-0 p-1">
        {state.loading && (
          <div className="text-gray-500">Loading recommendations…</div>
        )}
        {state.error && <div className="text-red-600">{state.error}</div>}

        {searching && searchState.loading && (
          <div className="text-gray-500">Searching…</div>
        )}
        {searching && searchState.error && (
          <div className="text-red-600">{searchState.error}</div>
        )}
        {!searching && !state.loading && !state.error && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {state.items.map((p) => (
              <div
                key={p.id || p.product_id || p.external_id}
                className="border rounded-lg p-4 hover:shadow-sm transition"
              >
                <div className="h-40 bg-gray-100 rounded mb-3 overflow-hidden flex items-center justify-center">
                  {p.image_url ? (
                    <img
                      src={p.image_url}
                      alt={p.title || p.name}
                      className="h-full object-cover"
                    />
                  ) : (
                    <div className="text-gray-400 text-sm">No image</div>
                  )}
                </div>

                <div className="font-medium line-clamp-2">
                  {p.title || p.name || 'Untitled'}
                </div>
                {typeof p.price !== 'undefined' && (
                  <div className="text-sm text-gray-900 mt-1">
                    ${Number(p.price).toFixed(2)}
                  </div>
                )}
                {p.description && (
                  <div className="text-sm text-gray-600 mt-1 line-clamp-2">
                    {p.description}
                  </div>
                )}

                <div className="mt-3 flex gap-2">
                  <button
                    className="px-3 py-1 rounded bg-blue-600 text-white text-sm"
                    onClick={async () => {
                      try {
                        const source = searching ? 'search' : 'cold_start';
                        await logView(p, source);
                        await sendRecommendationFeedback({
                          product: p,
                          action: 'clicked',
                          source,
                        });
                      } catch (e) {
                        console.debug('log view/feedback failed', e);
                      }
                    }}
                  >
                    View
                  </button>
                  <button
                    className="px-3 py-1 rounded bg-indigo-600 text-white text-sm"
                    onClick={async () => {
                      setSimilarState({
                        open: true,
                        base: p,
                        loading: true,
                        error: null,
                        items: [],
                      });
                      try {
                        const data = await getSimilarById(
                          p.id || p.product_id || p.external_id,
                          6
                        );
                        const items = Array.isArray(data?.results)
                          ? data.results
                          : data;
                        setSimilarState({
                          open: true,
                          base: p,
                          loading: false,
                          error: null,
                          items,
                        });
                      } catch (err) {
                        setSimilarState({
                          open: true,
                          base: p,
                          loading: false,
                          error: err?.message || 'Failed to load similar',
                          items: [],
                        });
                      }
                    }}
                  >
                    Similar
                  </button>
                  <button
                    className="px-3 py-1 rounded bg-emerald-600 text-white text-sm"
                    onClick={async () => {
                      try {
                        const source = searching ? 'search' : 'cold_start';
                        await logCartAdd(p, source);
                        await sendRecommendationFeedback({
                          product: p,
                          action: 'converted',
                          source,
                        });
                      } catch (e) {
                        console.debug('log cart/feedback failed', e);
                      }
                    }}
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
        {similarState.open && (
          <PopupLayout>
            <div style={{ padding: '1rem', minWidth: '60vw' }}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '.5rem',
                }}
              >
                <h3 style={{ margin: 0 }}>
                  Similar to:{' '}
                  {similarState.base?.title || similarState.base?.name}
                </h3>
                <button
                  onClick={() =>
                    setSimilarState({
                      open: false,
                      base: null,
                      loading: false,
                      error: null,
                      items: [],
                    })
                  }
                  style={{
                    padding: '.25rem .5rem',
                    borderRadius: 4,
                    border: '1px solid #ccc',
                  }}
                >
                  Close
                </button>
              </div>
              {similarState.loading && <div>Loading similar products…</div>}
              {similarState.error && (
                <div style={{ color: 'red' }}>{similarState.error}</div>
              )}
              {!similarState.loading && !similarState.error && (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {similarState.items.map((p) => (
                    <div
                      key={p.id || p.product_id || p.external_id}
                      className="border rounded-lg p-4"
                    >
                      <div className="h-32 bg-gray-100 rounded mb-3 overflow-hidden flex items-center justify-center">
                        {p.image_url ? (
                          <img
                            src={p.image_url}
                            alt={p.title || p.name}
                            className="h-full object-cover"
                          />
                        ) : (
                          <div className="text-gray-400 text-sm">No image</div>
                        )}
                      </div>
                      <div className="font-medium line-clamp-2">
                        {p.title || p.name || 'Untitled'}
                      </div>
                      {typeof p.price !== 'undefined' && (
                        <div className="text-sm text-gray-900 mt-1">
                          ${Number(p.price).toFixed(2)}
                        </div>
                      )}
                      <div className="mt-2 flex gap-2">
                        <button
                          className="px-2 py-1 rounded bg-blue-600 text-white text-xs"
                          onClick={async () => {
                            try {
                              const source = 'similar';
                              await logView(p, source);
                              await sendRecommendationFeedback({
                                product: p,
                                action: 'clicked',
                                source,
                              });
                            } catch (e) {
                              console.debug(
                                'log view/feedback failed (similar)',
                                e
                              );
                            }
                          }}
                        >
                          View
                        </button>
                        <button
                          className="px-2 py-1 rounded bg-emerald-600 text-white text-xs"
                          onClick={async () => {
                            try {
                              const source = 'similar';
                              await logCartAdd(p, source);
                              await sendRecommendationFeedback({
                                product: p,
                                action: 'converted',
                                source,
                              });
                            } catch (e) {
                              console.debug(
                                'log cart/feedback failed (similar)',
                                e
                              );
                            }
                          }}
                        >
                          Add to Cart
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </PopupLayout>
        )}
        {searching && !searchState.loading && !searchState.error && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {searchState.items.map((p) => (
              <div
                key={p.id || p.product_id || p.external_id}
                className="border rounded-lg p-4 hover:shadow-sm transition"
              >
                <div className="h-40 bg-gray-100 rounded mb-3 overflow-hidden flex items-center justify-center">
                  {p.image_url ? (
                    <img
                      src={p.image_url}
                      alt={p.title || p.name}
                      className="h-full object-cover"
                    />
                  ) : (
                    <div className="text-gray-400 text-sm">No image</div>
                  )}
                </div>
                <div className="font-medium line-clamp-2">
                  {p.title || p.name || 'Untitled'}
                </div>
                {typeof p.price !== 'undefined' && (
                  <div className="text-sm text-gray-900 mt-1">
                    ${Number(p.price).toFixed(2)}
                  </div>
                )}
                {p.description && (
                  <div className="text-sm text-gray-600 mt-1 line-clamp-2">
                    {p.description}
                  </div>
                )}
                <div className="mt-3 flex gap-2">
                  <Button
                    className="text-sm"
                    style={{ ...theme.buttons.emphasis }}
                    onClick={async () => {
                      try {
                        const source = 'search';
                        await logView(p, source);
                        await sendRecommendationFeedback({
                          product: p,
                          action: 'clicked',
                          source,
                        });
                      } catch (e) {
                        console.debug('log view/feedback failed (search)', e);
                      }
                    }}
                  >
                    View
                  </Button>
                  <Button
                    className="text-sm"
                    style={{ ...theme.buttons.splash }}
                    onClick={async () => {
                      try {
                        const source = 'search';
                        await logCartAdd(p, source);
                        await sendRecommendationFeedback({
                          product: p,
                          action: 'converted',
                          source,
                        });
                      } catch (e) {
                        console.debug('log cart/feedback failed (search)', e);
                      }
                    }}
                  >
                    Add to Cart
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Row>
    </Col>
  );
}

export default RecommendedProducts;
