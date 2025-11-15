import { useEffect } from "react";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import CloseButton from "react-bootstrap/CloseButton";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import logoUrl from "/logo.svg?url";
import Image from "react-bootstrap/Image";
import { useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import CloseButton from 'react-bootstrap/CloseButton';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import logoUrl from '/logo.svg?url';

function FocusedProduct({
  product = {},
  recommendations = [],
  onAddToCart,
  onBuyNow,
  onWishlist,
  onMoreLikeThis,
  onClose,
}) {
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

  // sample recommendations
  const recs = recommendations.length
    ? recommendations
    : Array.from({ length: 12 }).map((_, i) => ({
      id: i,
      title:
        i % 3 === 0
          ? 'Bought Together'
          : 'Similar Item by Different Category',
    }));


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
        borderRadius: 4,
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
          borderRadius: 4,
          padding: '.25rem .5rem',
          fontWeight: 600,
        }}
      />

      <Container
        fluid
        className="h-100"
      >
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
                <img
                  src={product.imageUrl}
                  alt={`Image of ${name}`}
                  style={{
                    maxWidth: '100%',
                    maxHeight: '100%',
                    objectFit: 'contain',
                  }}
                />
              ) : (
                <Image
                  src={logoUrl}
                  alt="Logo"
                  style={{ height: "100%", maxHeight: "3rem", objectFit: "contain" }}
                  style={{
                    height: '100%',
                    maxHeight: '3rem',
                    objectFit: 'contain',
                  }}
                />
              )}
            </div>

            <div>
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
                style={{ ...primaryBtn }}
                onClick={onAddToCart}
              >
                Add to cart
              </Button>
              <Button
                variant="dark"
                style={{ ...darkBtn }}
                onClick={onBuyNow}
              >
                Buy
              </Button>
              <Button
                variant="light"
                style={{ ...mutedBtn }}
                onClick={onWishlist}
              >
                Wishlist
              </Button>
              <Button
                variant="light"
                style={{ ...mutedBtn }}
                onClick={onMoreLikeThis}
              >
                More Like This
              </Button>
            </div>
          </Col >

          {/* Right column: recommendations grid */}
          < Col
            md={7}
            className="overflow-auto"
          >
            <div
              className="d-grid"
              style={{
                gridTemplateColumns: 'repeat(3, minmax(0, 1fr))',
                gap: '1rem',
                alignContent: 'start',
                height: '100%',
              }}
            >
              {recs.map((rec, idx) => (
                <div
                  key={rec.id ?? idx}
                  style={{
                    minHeight: 72,
                    background: '#f3f5f7',
                    border: '1px dashed #b9c3cf',
                    borderRadius: 6,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    textAlign: 'center',
                    padding: '.75rem',
                    fontSize: 12,
                    fontWeight: 700,
                    color: '#384554',
                  }}
                >
                  {rec.title}
                </div>
              ))}
            </div>
          </Col >
        </Row >
      </Container >
    </Card >
  );


  // Reusable button styles
  const baseBtn = {
    border: '1px solid transparent',
    borderRadius: 6,
    padding: '.5rem .9rem',
    cursor: 'pointer',
    fontWeight: 700,
  };

  const primaryBtn = {
    ...baseBtn,
    background: '#4c8bf5',
    borderColor: '#2f6fda',
    color: 'white',
  };

  const darkBtn = {
    ...baseBtn,
    background: '#1f2937',
    color: 'white',
  };

  const mutedBtn = {
    ...baseBtn,
    background: '#e8eef6',
    color: '#1f2937',
    borderColor: '#c8d3e0',
  };

  export default FocusedProduct;
