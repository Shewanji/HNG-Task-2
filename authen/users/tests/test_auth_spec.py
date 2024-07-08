# users/tests.py

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User, Organisation
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_register_user_successfully():
    client = APIClient()
    url = reverse('register')
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'accessToken' in response.data['data']
    assert Organisation.objects.filter(name="John's Organisation").exists()

@pytest.mark.django_db
def test_login_user_successfully():
    # Create a user for testing
    User.objects.create_user(email='john.doe@example.com', firstName='John', lastName='Doe', password='password123')

    # Initialize the API client and prepare the login request
    client = APIClient()
    url = reverse('login')
    data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }

    # Send the login request and check the response
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

    # Extract the access token from the response data
    access_token = response.data['data']['accessToken']

    # Ensure the access token is valid
    decoded_token = RefreshToken(access_token).payload

    # Assert that the token payload contains necessary fields (e.g., userId)
    assert 'userId' in decoded_token
@pytest.mark.django_db
def test_register_user_with_missing_fields():
    client = APIClient()
    url = reverse('register')
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "",
        "password": "password123",
        "phone": "1234567890"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.django_db
def test_register_user_with_duplicate_email():
    User.objects.create_user(email='john.doe@example.com', firstName='John', lastName='Doe', password='password123')
    client = APIClient()
    url = reverse('register')
    data = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "0987654321"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
