from django.test import TestCase, override_settings
from django.test.client import Client
from rest_framework import status

from .models import People


class PeopleTestCase(TestCase):
    content_type = 'application/json'
    base_url = '/sample/people/'
    model = People

    # ======================================================================

    @override_settings(DEBUG=True)
    def test_integration(self):
        client = Client()

        response = client.get(path=self.base_url, content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, "1 status")
        self.assertEquals(response.data, [], "1 data")

        people = []
        people.append({
            'first_name': 'first_name_0',
            'last_name': 'last_name_0',
        })
        people_in_db = []
        id_created = 1
        response = client.post(path=self.base_url, data=people[-1], content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, "2 status")
        self.assertEquals(response.data, {'id': id_created}, "2 data")
        people_in_db.append(people[-1])
        people_in_db[-1]['id'] = id_created

        response = client.get(path=self.base_url, content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, "3 status")
        self.assertEquals(response.data, people_in_db, "3 data")

        response = client.get(path=self.base_url + str(id_created) + '/', content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, "4 status")
        self.assertEquals(response.data, people_in_db[id_created-1], "4 data")

        people[id_created-1]['first_name'] += '_another'
        people[id_created-1]['last_name'] += '_another'
        response = client.put(path=self.base_url + str(id_created) + '/', data=people[id_created-1], content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, "5 status")
        self.assertEquals(response.data, None, "5 data")
        people_in_db[id_created-1]['first_name'] = people[id_created-1]['first_name']
        people_in_db[id_created-1]['last_name'] = people[id_created-1]['last_name']

        response = client.get(path=self.base_url + str(id_created) + '/', content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, "6 status")
        self.assertEquals(response.data, people_in_db[id_created-1], "6 data")

        del people[id_created-1]
        response = client.delete(path=self.base_url + str(id_created) + '/', content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, "7 status")
        self.assertEquals(response.data, None, "7 data")
        del people_in_db[id_created-1]

        response = client.get(path=self.base_url, content_type=self.content_type, HTTP_ACCEPT=self.content_type)
        self.assertEquals(response.status_code, status.HTTP_200_OK, "8 status")
        self.assertEquals(response.data, people_in_db, "8 data")
