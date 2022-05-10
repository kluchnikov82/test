from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.utils import json

from .models import Check, Printer
from .serializers import CheckSzr, CheckListSzr
import os.path
from django.conf import settings
from django.http import JsonResponse, HttpResponse


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
        try:
            Printer.objects.get(api_key=request.query_params['api_key'])
        except Printer.DoesNotExist:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'message': 'Не существует принтера с таким api_key'}
            )

        checks = Check.objects.filter(printer_id__api_key=request.query_params['api_key'], uuid=request.query_params['check_id'])
        if not checks.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'Данного чека не существует'}
            )

        data = ''
        for check in checks:
            if os.path.exists(str(settings.BASE_DIR) + '/media/' + str(check.order['id']) + '_client.pdf'):
                data = str(check.order['id']) + '_client.pdf'
            if os.path.exists(str(settings.BASE_DIR) + '/media/' + str(check.order['id']) + '_kitchen.pdf'):
                data += '; ' + str(check.order['id']) + '_kitchen.pdf'

        return HttpResponse(json.dumps({"data": data}), content_type='application/json')




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
