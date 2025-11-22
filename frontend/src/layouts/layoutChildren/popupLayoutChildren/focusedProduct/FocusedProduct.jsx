import { useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import { useTheme } from '@resources/themes/themeContext';
import logoUrl from '/logo.svg?url';
import CloseButton from '../../button/CloseButton';

function FocusedProduct({
  product = {},
  onAddToCart,
  onBuyNow,
  onMoreLikeThis,
  onClose,
}) {
  const { theme } = useTheme();
  // Close on esc
  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'Escape' && onClose) onClose();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose]);

  const name = product?.name || 'Item Name';
  const description =
    product?.description ||
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus vel sem magna. Vivamus velit iaculis, luctus libero vel, porta tincidunt magna. Ut placerat sagittis massa, at laoreet velit vehicula ut.';

  return (
    <Card
      role="dialog"
      aria-modal="true"
      aria-label={`Details for ${name}`}
      className="p-3 shadow position-relative m-auto"
      style={{
        width: '100%',
        height: '100%',
        backgroundColor: '#fffffb',
        color: '#222',
        borderRadius: theme.props.bR_less,
      }}
    >
      {/* Close button */}
      <CloseButton
        onClick={onClose}
        aria-label="Close"
        className="position-absolute"
        style={{
          right: 12,
          top: 8,
          background: '#e8eef6',
          border: '1px solid #9ab',
          borderRadius: theme.props.bR_less,
          padding: '.25rem .5rem',
          fontWeight: 600,
        }}
      />
      <Card.Body className="h-100">
        <Row className="h-100">
          {/* Left column: image/icon + title/description */}
          <Col
            md={5}
            className="d-flex flex-column gap-3"
          >
            <div
              className="d-flex align-items-center justify-content-center"
              style={{
                flex: '0 0 auto',
                width: '100%',
                aspectRatio: '4 / 3',
                background: '#e6f0fb',
                border: '2px solid #a7c3e8',
                borderRadius: 6,
              }}
            >
              {product?.imageUrl ? (
                <Card.Img
                  src={product.imageUrl}
                  alt={`Image of ${name}`}
                  style={{
                    objectFit: 'cover',
                  }}
                />
              ) : (
                <Card.Img
                  src={logoUrl}
                  alt="Logo"
                  style={{
                    objectFit: 'cover',
                  }}
                />
              )}
            </div>

            <div className="d-none">
              <h2 style={{ margin: 0 }}>{name}</h2>
              <div style={{ fontWeight: 600, marginTop: '.25rem' }}>
                Description:
              </div>
              <p style={{ marginTop: '.25rem', lineHeight: 1.35 }}>
                {description}
              </p>
            </div>

            {/* Action buttons */}
            <div className="mt-auto d-flex flex-wrap gap-2">
              <Button
                variant="primary"
                style={{ ...theme.buttons.contrast }}
                onClick={onAddToCart}
              >
                Add to cart
              </Button>
              <Button
                variant="dark"
                style={{ ...theme.buttons.splash }}
                onClick={onBuyNow}
              >
                Buy
              </Button>
              <Button
                variant="light"
                style={{ ...theme.buttons.muted }}
                onClick={onMoreLikeThis}
              >
                More Like This
              </Button>
            </div>
          </Col>

          {/* Right column: recommendations grid */}
          <Col
            md={7}
            className="overflow-auto"
          ></Col>
        </Row>
      </Card.Body>
    </Card>
  );
}
export default FocusedProduct;
