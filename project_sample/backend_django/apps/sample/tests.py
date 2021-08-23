from django.test import TestCase, override_settings
from django.test.client import Client
from rest_framework import status

from .models import People


class PeopleTestCase(TestCase):
    content_type = 'application/json'
    base_url = '/sample/people/'
    model = People

    # ======================================================================

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # ======================================================================

    @override_settings(DEBUG=True)
    def test(self):
        client = Client()

    # ----- Integration Test -----

        # GET People
        response = client.get(path=self.base_url,
                              content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, '1 status')
        self.assertEquals(response.data, [], '1 data')

        # POST
        data_person = {
            'first_name': 'first_name_0',
            'last_name': 'last_name_0',
        }
        person_in_db = data_person.copy()
        person_in_db['id'] = 1
        response = client.post(path=self.base_url,
                               data=data_person, content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, '2 status')
        self.assertEquals(response.data, {'id': person_in_db['id']}, '2 data')

        # GET People
        response = client.get(path=self.base_url,
                              content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, '3 status')
        self.assertEquals(response.data, [person_in_db], '3 data')

        # GET Person
        response = client.get(path=self.base_url + str(person_in_db['id']) + '/',
                              content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, '4 status')
        self.assertEquals(response.data, person_in_db, '4 data')

        # PUT
        data_person['first_name'] += '_another'
        data_person['last_name'] += '_another'
        person_in_db['first_name'] = data_person['first_name']
        person_in_db['last_name'] = data_person['last_name']
        response = client.put(path=self.base_url + str(person_in_db['id']) + '/',
                              data=data_person, content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, '5 status')
        self.assertEquals(response.data, None, '5 data')

        # GET Person
        response = client.get(path=self.base_url + str(person_in_db['id']) + '/',
                              content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, '6 status')
        self.assertEquals(response.data, person_in_db, '6 data')

        # DELETE
        response = client.delete(path=self.base_url + str(person_in_db['id']) + '/',
                                 content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, '7 status')
        self.assertEquals(response.data, None, '7 data')

        # GET People
        response = client.get(path=self.base_url,
                              content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, '8 status')
        self.assertEquals(response.data, [], '8 data')

    # ----- Indexing Test -----

        # WORSE
        self.model.objects.create(first_name='first_name_0', last_name='last_name_0')
        self.model.objects.create(first_name='first_name_1', last_name='last_name_1')

        # BETTER
        self.model.objects.bulk_create([
            self.model(first_name='first_name_2', last_name='last_name_2'),
            self.model(first_name='first_name_3', last_name='last_name_3')
        ])

        person_expected = {
            'id': 4,
            'first_name': 'first_name_2',
            'last_name': 'last_name_2',
        }

        response = client.get(path=self.base_url + '?first_name=' + person_expected['first_name'],
                              content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.data, [person_expected], 'first_name')

        response = client.get(path=self.base_url + '?last_name=' + person_expected['last_name'],
                              content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.data, [person_expected], 'last_name')
