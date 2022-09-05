import json
from urllib import response

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .serializers import AccountSerializer

User = get_user_model()


class RegisterTest(APITestCase):
    """ Test module for  register new user """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.signup_url = reverse('api_register')

    def test_register_serializer(self):
        data = {
            'username': 'employee6',
            'email': 'employee6@company.com',
            'first_name': "Alex",
            'last_name': 'Tailor',
            'password': 'employee6',
            'password2': 'employee6',
        }
        serializer = AccountSerializer(data)
        self.assertEqual(serializer.data['username'], data['username'])
        self.assertEqual(serializer.data['email'], data['email'])

    def test_api_registeration(self):
        data = {
            'username': 'employee6',
            'email': 'employee6@company.com',
            'first_name': "Alex",
            'last_name': 'Tailor',
            'password': 'employee6',
            'password2': 'employee6',
        }

        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registeration_fail(self):

        data = {
            'username': 'employee6',
            'email': 'employee6@company.com',
            'first_name': "Alex",
            'last_name': 'Tailor',
            'password': 'asdas',
            'password2': 'employee6',
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_is_staff(self):
        data = {
            'username': 'employee6',
            'email': 'employee6@company.com',
            'first_name': "Alex",
            'last_name': 'Tailor',
            'password': 'employee6',
            'password2': 'employee6',
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        test_user = User.objects.get(username='employee6')
        self.assertTrue(test_user.is_staff)

    def test_user_is_staff_false(self):
        data = {
            'username': 'employee6',
            'email': 'employee6@gmail.com',
            'first_name': "Alex",
            'last_name': 'Tailor',
            'password': 'employee6',
            'password2': 'employee6',
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        test_user = User.objects.get(username='employee6')
        self.assertFalse(test_user.is_staff)


class ListUsersTest(APITestCase):
    """ Test module for  register new user """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.list_users_url = reverse('list_users')
        cls.signup_url = reverse('api_register')

    def test_list_users(self):
        "This test should return users ordered by is_staff"

        response = self.client.get(self.list_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users(self):
        "This test should return users ordered by is_staff"

        user1 = {
            "username": "alex1",
            "email": "alex1@gmail.com",
            "first_name": "Alex",
            "last_name": "Tailor",
            'password': 'passAlex1',
            'password2': 'passAlex1',
        }
        user2 = {
            "username": "Luke",
            "email": "emp2@COMPANY.com",
            "first_name": "luke",
            "last_name": "Tailor",
            'password': 'passLuke1',
            'password2': 'passLuke1',
        }
        user3 = {
            "username": "James",
            "email": "James@company.com",
            "first_name": "James",
            "last_name": "Tailor",
            'password': 'James123',
            'password2': 'James123',
        }

        res_user1 = self.client.post(self.signup_url, user1, format="json")
        res_user2 = self.client.post(self.signup_url, user2, format="json")
        res_user3 = self.client.post(self.signup_url, user3, format="json")

        response = self.client.get(self.list_users_url)

        self.assertEqual(len(response.data['users']), 3)

        "Check if users are ordered, first users's is_staff should be True"
        user1_is_staff = response.data['users'][0]['is_staff']
        user2_is_staff = response.data['users'][1]['is_staff']
        user3_is_staff = response.data['users'][2]['is_staff']
        self.assertTrue(user1_is_staff)
        self.assertTrue(user2_is_staff)
        self.assertFalse(user3_is_staff)
