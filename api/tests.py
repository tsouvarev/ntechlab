from http import HTTPStatus

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse_lazy

from .models import Neighbour


class GetNeighbourTestCase(TestCase):
    url = reverse_lazy('neighbours')

    def test_get_neighbours_with_bad_params(self):
        bad_params = [
            {'n': 1},
            {'n': 1000, 'x': 1, 'y': 1},
            {'n': 0, 'x': 1, 'y': 1},
            {'x': 1},
            {'y': 1},
            {'x': 1, 'y': 1},
        ]

        for params in bad_params:
            with self.subTest(params=params):
                response = self.client.get(self.url, data=params)

            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_neighbours(self):
        # far away
        Neighbour.objects.create(name='kitty', point=Point(1, 3))
        # not so far
        Neighbour.objects.create(name='sugar', point=Point(1, 2))
        # really close
        Neighbour.objects.create(name='mimmy', point=Point(1, 1))

        response = self.client.get(self.url, data={'n': 2, 'x': 1, 'y': 1})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertJSONEqual(response.content, ['mimmy', 'sugar'])
