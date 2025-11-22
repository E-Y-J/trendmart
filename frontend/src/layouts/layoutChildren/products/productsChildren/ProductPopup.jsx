import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { useTheme } from '@styles/themeContext';
import PopupCloseButton from '@children/button/CloseButton';
import Logo from '@children/logo/Logo';

function ProductPopup({
    product,
    show,
    onClose,
    onAddToCart,
    onBuyNow,
    onMoreLikeThis,
}) {
    const { theme } = useTheme();
    if (!product) return null;

    const { name, imageUrl, description, price, tags, score } = product;
    const priceDisplay = `$${Number(price || 0).toFixed(2)}`;

    return (
        <Modal
            show={show}
            onHide={onClose}
            centered
            size="lg"
            aria-label={`Details for ${name}`}
        >
            <Modal.Header>
                <Modal.Title style={{ fontSize: '1.1rem' }}>{name}</Modal.Title>
            </Modal.Header>

            <PopupCloseButton
                onClick={onClose}
                style={{ zIndex: 999, margin: '4px' }}
            />

            <Modal.Body>
                <div className="d-flex flex-column flex-md-row gap-3">
                    {/* Image */}
                    <div
                        style={{
                            flex: '0 0 320px',
                            background: '#e9eef2',
                            borderRadius: 6,
                            overflow: 'hidden',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            aspectRatio: '4 / 3',
                        }}
                    >
                        {imageUrl ? (
                            <img
                                src={imageUrl}
                                alt={name}
                                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                            />
                        ) : (
                            <div style={{ fontSize: '.75rem', color: '#667' }}>
                                No Image Available
                            </div>
                        )}
                    </div>

                    {/* Details */}
                    <div className="flex-grow-1 d-flex flex-column gap-2">
                        <div className="fw-semibold" style={{ fontSize: '.9rem' }}>
                            Price: {priceDisplay}
                        </div>

                        {/* AI Recommendation Score */}
                        {typeof score === 'number' && score > 0 ? (
                            <div style={{ fontSize: '.7rem', color: '#333' }}>
                                <span style={{ fontWeight: 600 }}>AI Match:</span>{' '}
                                {(score * 100).toFixed(0)}%
                                <span style={{ marginLeft: 6, fontSize: '.65rem', color: '#666' }}>
                                    {score >= 0.8
                                        ? 'High'
                                        : score >= 0.55
                                            ? 'Medium'
                                            : 'Low'}
                                </span>
                            </div>
                        ) : (
                            <div style={{ fontSize: '.65rem', color: '#777' }}>
                                AI match pending
                            </div>
                        )}

                        {tags && (
                            <div style={{ fontSize: '.65rem', color: '#444' }}>Tags: {tags}</div>
                        )}

                        <div style={{ fontSize: '.75rem', lineHeight: 1.3 }}>
                            {description || 'No description available.'}
                        </div>
                    </div>
                </div>
            </Modal.Body>

            <Modal.Footer className="d-flex justify-content-between">
                <div className="d-flex gap-2">
                    <Button
                        variant="dark"
                        style={{ ...theme.buttons.splash }}
                        onClick={() => onBuyNow?.(product)}
                    >
                        Buy Now
                    </Button>

                    {/* Right: TrendMart logo as Add-to-Cart */}
                    {onAddToCart && (
                        <button
                            type="button"
                            onClick={() => onAddToCart(product)}
                            aria-label="Add to cart"
                            className="border-0 p-0 m-0"
                            style={{
                                width: 56,
                                height: 56,
                                borderRadius: '50%',
                                overflow: 'hidden',
                                backgroundColor: theme.colors.primaryBg || '#0a1f45',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                            }}
                        >
                            {/* You can pass details={false} or true depending on look you want */}
                            <Logo details={false} />
                        </button>
                    )}
                    {onMoreLikeThis && (
                        <Button
                            variant="outline-secondary"
                            style={{ ...theme.buttons.muted }}
                            onClick={() => onMoreLikeThis(product)}
                        >
                            More Like This
                        </Button>
                    )}

                </div>
            </Modal.Footer>
        </Modal>
    );
}

export default ProductPopup;