from rest_framework import generics, status
from rest_framework_api_key.models import APIKey
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from .models import Check, Printer
from .serializers import CheckSzr, CheckListSzr


class NewChecksView(generics.ListAPIView):

    serializer_class = CheckListSzr

    def get(self, request, *args, **kwargs):
        try:
            Printer.objects.get(api_key=request.query_params['api_key'])
        except Printer.DoesNotExist:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'message': 'Не существует принтера с таким api_key'}
            )

        checks = Check.objects.filter(printer_id__api_key=request.query_params['api_key'])
        if not checks.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'Для данной точки не настроено ни одного принтера'}
            )

        serializer = CheckListSzr(checks, many=True)

        return Response(data={'checks:': serializer.data}, status=status.HTTP_200_OK)


class CheckView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        data = request.data
        api_key, key = APIKey.objects.create_key(name="my-remote-service")
        print(api_key)
        return Response(data, status=status.HTTP_200_OK)


class CreateChecksView(generics.CreateAPIView):
    # permission_classes = [HasAPIKey]
    queryset = Check.objects.all()
    serializer_class = CheckSzr

    def post(self, request, *args, **kwargs):
        record = {}
        data = request.data
        record['order'] = data

        printers = Printer.objects.filter(point_id=data['point_id'])
        if not printers.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'Для данной точки не настроено ни одного принтера'}
            )

        order = Check.objects.filter(order__id=data['id'])
        if order.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'Для данного заказа уже созданы чеки'}
            )

        for printer in printers:
            serializer = self.get_serializer(context={'request': printer}, data=record)
            serializer.is_valid(raise_exception=True)
            c = serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data={'message': 'Чеки успешно созданы'}
        )
