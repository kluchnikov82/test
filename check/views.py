from django.conf import settings
from rest_framework import generics, status
from rest_framework_api_key.models import APIKey
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from .models import Check, Printer
from .serializers import CheckSzr, CheckListSzr
import django_rq
from .tasks import *
import pdfkit
import os
from django.template.loader import render_to_string, get_template



class NewChecksView(generics.ListAPIView):

    serializer_class = CheckListSzr

    def get(self, request, *args, **kwargs):
        queue = django_rq.get_queue('default')
        queue.enqueue(task)
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
       pass



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
