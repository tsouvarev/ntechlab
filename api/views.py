from http import HTTPStatus

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.views import View

from .forms import NeighbourListForm, NeighbourCreateForm
from .models import Neighbour


WGS84_SRID = 4326


class NeighbourView(View):
    def get(self, request):
        form = NeighbourListForm(request.GET)
        if not form.is_valid():
            return JsonResponse(
                form.errors.as_json(), safe=False,
                status=HTTPStatus.BAD_REQUEST,
            )

        point = Point(
            form.cleaned_data['x'],
            form.cleaned_data['y'],
            srid=WGS84_SRID,
        )
        n = form.cleaned_data['n']

        ordered_neighbours = Neighbour.objects.annotate(
            distance=Distance('point', point),
        ).order_by('distance')

        return JsonResponse(
            list(map(serialize_neighbour, ordered_neighbours[:n])), safe=False,
        )

    def post(self, request):
        form = NeighbourCreateForm(request.POST)
        if not form.is_valid():
            return JsonResponse(
                form.errors.as_json(), safe=False,
                status=HTTPStatus.BAD_REQUEST,
            )

        point = Point(
            form.cleaned_data['x'],
            form.cleaned_data['y'],
            srid=WGS84_SRID,
        )
        name = form.cleaned_data['name']

        Neighbour.objects.create(name=name, point=point)

        return JsonResponse({}, status=HTTPStatus.CREATED)


def serialize_neighbour(neighbour):
    return neighbour.name
