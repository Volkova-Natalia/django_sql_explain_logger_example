from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import People
from .serializers import PeopleSerializer
from .utils import sql_explain_logger, server_logger


# ======================================================================


class BaseView(APIView):
    content_type = 'application/json'

    # --------------------------------------------------

    def response_200(self, *, data):
        return Response(
            data=data,
            status=status.HTTP_200_OK,
            content_type=self.content_type
        )

    def response_201(self, *, data):
        return Response(
            data=data,
            status=status.HTTP_201_CREATED,
            content_type=self.content_type
        )

    def response_204(self):
        return Response(
            data=None,
            status=status.HTTP_204_NO_CONTENT,
            content_type=self.content_type
        )

    # --------------------------------------------------

    def response_400(self, *, data):
        return Response(
            data=data,
            status=status.HTTP_400_BAD_REQUEST,
            content_type=self.content_type
        )

    def response_401(self):
        return Response(
            data=None,
            status=status.HTTP_401_UNAUTHORIZED,
            content_type=self.content_type
        )

    def response_403(self):
        return Response(
            data=None,
            status=status.HTTP_403_FORBIDDEN,
            content_type=self.content_type
        )

    def response_404(self):
        return Response(
            data=None,
            status=status.HTTP_404_NOT_FOUND,
            content_type=self.content_type
        )

    # --------------------------------------------------


# ======================================================================


class PeopleView(BaseView):
    model = People
    get_serializer = PeopleSerializer
    post_serializer = PeopleSerializer

    # --------------------------------------------------

    def get(self, request, *args, **kwargs):
        objects = self.model.objects.all()[:]
        serializer = self.get_serializer(objects, context={'request': request}, many=True)
        result = self.response_200(data=serializer.data)

        sql_explain_logger()
        server_logger(request, result)
        return result

    # --------------------------------------------------

    def post(self, request, *args, **kwargs):
        serializer = self.post_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            object = serializer.save()
            result = self.response_201(data={'id': object.id})
            result['Location'] = object.get_absolute_url()
        else:
            result = self.response_400(data=serializer.errors)

        sql_explain_logger()
        server_logger(request, result)
        return result

    # --------------------------------------------------


# ======================================================================


class PersonView(BaseView):
    model = People
    get_serializer = PeopleSerializer
    put_serializer = PeopleSerializer
    delete_serializer = PeopleSerializer

    # --------------------------------------------------

    def _get_object(self, *, id):
        try:
            object = self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None
        return object

    # --------------------------------------------------

    def get(self, request, id, *args, **kwargs):
        object = self._get_object(id=id)
        if not object:
            result = self.response_404()
        else:
            serializer = self.get_serializer(object, context={'request': request})
            result = self.response_200(data=serializer.data)

        sql_explain_logger()
        server_logger(request, result)
        return result

    # --------------------------------------------------

    def put(self, request, id, *args, **kwargs):
        object = self._get_object(id=id)
        if not object:
            result = self.response_404()
        else:
            serializer = self.put_serializer(object, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                result = self.response_200(data=None)
            else:
                result = self.response_400(data=serializer.errors)

        sql_explain_logger()
        server_logger(request, result)
        return result

    # --------------------------------------------------

    def delete(self, request, id, *args, **kwargs):
        object = self._get_object(id=id)
        if not object:
            result = self.response_404()
        else:
            object.delete()
            result = self.response_204()

        sql_explain_logger()
        server_logger(request, result)
        return result

    # --------------------------------------------------


