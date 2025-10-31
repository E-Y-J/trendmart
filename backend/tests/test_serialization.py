from conftest import *
from backend.models.serializers import product_to_dict as canonical
from backend.models import product_to_dict


class DummyProduct:
    id = 1
    sku = "SKU123"
    name = "Test Product"
    description = "A product for testing."
    price = 19.99
    rating = 4.5
    tags = "test, sample, dummy"
    product_img = "http://example.com/image.jpg"
    images = []
    times_click_on = 42
    subcategory = None  # Simplified for this test


def test_product_to_dict_equivalence():
    product = DummyProduct()
    dict1 = product_to_dict(product)
    dict2 = canonical(product)
    assert isinstance(dict1, dict)
    assert isinstance(dict2, dict)
    assert dict1['id'] == 1
    assert dict1['sku'] == "SKU123"
    assert dict1['name'] == "Test Product"
    assert dict1['description'] == "A product for testing."
    assert dict1['price'] == 19.99
    assert dict1['rating'] == 4.5
    assert dict1['tags'] == ['test', 'sample', 'dummy']
    assert dict1['primary_image'] == "http://example.com/image.jpg"
    assert dict1['times_click_on'] == 42

    print(
        f'{DummyProduct.__name__} serialization test passed: {dict1["name"]} -> {dict1}')
