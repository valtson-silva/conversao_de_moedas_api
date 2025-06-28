import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.cache import cache

from api.models import ConversionHistory
from api.coversion_services import convert_currency_coin


User = get_user_model()


def create_conversion_history(from_currency, to_currency, amount):
    conversion = convert_currency_coin(from_currency, to_currency, amount)
    data = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "convert_amount": conversion["convert_amount"],
        "conversion_rate": conversion["conversion_rate"]
    }
    return ConversionHistory.objects.create(**data)


def get_authenticated_client():
    client = APIClient()
    User.objects.create_user(email="testuser@email.com", password="testpass")
    token_url = reverse('token_access')  
    response = client.post(token_url, {"email": "testuser@email.com", "password": "testpass"})
    access_token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.mark.django_db
def test_conversion_crypto_create():
    client = get_authenticated_client()
    url = reverse('conversion_crypto')

    response = client.post(url, {
        "from_currency": "BTC",
        "to_currency": "ETH",
        "amount": 10
    }, format="json")

    assert response.status_code == 201
    assert response.data['from_currency'] == "BTC"


@pytest.mark.django_db
def test_conversion_crypto_create_invalid_data():
    client = get_authenticated_client()
    url = reverse('conversion_crypto')

    response = client.post(url, {
        "from_currency": "BTC",
        "to_currency": "ETH",
        "amount": "abc"
    }, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_conversion_coin_create():
    client = get_authenticated_client()
    url = reverse('conversion_coin')

    response = client.post(url, {
        "from_currency": "USD",
        "to_currency": "EUR",
        "amount": 10
    }, format="json")

    assert response.status_code == 201
    assert response.data['from_currency'] == "USD"


@pytest.mark.django_db
def test_conversion_coin_create_invalid_data():
    client = get_authenticated_client()
    url = reverse('conversion_coin')

    response = client.post(url, {
        "from_currency": "USD",
        "to_currency": "EUR",
        "amount": "abc"
    }, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_create_invalid_data():
    client = APIClient()
    url = reverse('register_user')

    response = client.post(url, {
        "username": "user",
        "email": "user@example.com",
        "password": ""
    }, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_conversion_list_view():
    client = get_authenticated_client()
    url = reverse('conversion_list')

    create_conversion_history("USD", "EUR", 10)

    response = client.get(url, format="json")

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_conversion_list_view_cache():
    client = get_authenticated_client()
    url = reverse('conversion_list')

    create_conversion_history("USD", "EUR", 10)

    response = client.get(url, format="json")

    assert response.status_code == 200
    assert len(response.data) == 1

    cache_list = cache.get("conversion_list")
    assert cache_list is not None
    

@pytest.mark.django_db
def test_conversion_delete_view():
    client = get_authenticated_client()
    conversion = create_conversion_history("USD", "EUR", 10)
    
    url = reverse("conversion_delete", args=[conversion.id])
    
    response = client.delete(url)
    
    assert response.status_code == 204
    assert not ConversionHistory.objects.filter(id=conversion.id).exists()
    