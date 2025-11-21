import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import { useTheme } from '@styles/themeContext';

function ProductCard({
    product,
    onBuy,
    onView,
    onAddToCart,
    onMoreLikeThis,
}) {
    const { theme } = useTheme();
    if (!product) return null;

    const { id, name, imageUrl, description, price, score } = product;
    const priceDisplay = `$${Number(price || 0).toFixed(2)}`;

    return (
        <Card
            className='p-2 d-flex flex-column h-100 shadow-sm'
            data-product-id={id}
            style={{ borderRadius: 6, background: '#fffffd' }}
        >
            {/* Product Image */}
            <div style={{
                width: '100%',
                aspectRatio: '4 / 3',
                background: '#e9eef2',
                borderRadius: 4,
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
            }}>
                {imageUrl ? (
                    <img src={imageUrl} alt={name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                ) : (
                    <div style={{ fontSize: '.75rem', color: '#667' }}>{'No Image Available'}</div>
                )}
            </div>

            {/* name and short subtitle/specs */}
            <div className='mt-2 fw-semibold' style={{ lineHeight: 1.2 }}>
                {name}
            </div>
            {description && (
                <div className='text-muted' style={{ fontSize: '.7rem', lineheight: 1.2, maxHeight: '2.4rem', overflow: 'hidden', }}>
                    {description}
                </div>
            )}

            {/* Recommendation Score */}
            {score !== undefined && (
                <div className='mt-1' style={{ fontSize: '.65rem', color: '#555' }}>
                    AI Recom Score: {(score * 100).toFixed(0)}%
                </div>
            )}

            {/* Price on bottom left . add to cart and buy now button on bottom right */}
            <Button size='sm' variant='dark' style={{ ...theme.buttons.splash, fontSize: '.75rem' }}
                onClick={(e) => {
                    e.stopPropagation();
                    onBuy?.(product);
                }}>
                Buy Now
            </Button>
            {onAddToCart && (
                <Button size='sm' variant='outline-primary' style={{ fontSize: '.75rem' }}
                    onClick={(e) => {
                        e.stopPropagation();
                        onAddToCart?.(product);
                    }}>
                    Cart
                </Button>
            )}
        </Card>
    )
}

export default ProductCard;