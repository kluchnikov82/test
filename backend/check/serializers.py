from rest_framework import serializers
from .models import *


# class PrinterSzr(serializers.ModelSerializer):
#     """
#         Сериализатор модели принтер
#     """
#     class Meta:
#         model = Printer
#         fields = (
#         )


class CheckSzr(serializers.ModelSerializer):
    """
        Сериализатор модели чек
    """
    def create(self, validated_data):
        printer = self.context['request']
        type_check = self.context['request'].check_type
        order = validated_data.get('order', '')
        status = 'Новый'
        c = Check.objects.create(
            printer_id=printer,
            type_check=type_check,
            order=order,
            status=status
        )

        return c

    class Meta:
        model = Check
        fields = (
            'printer_id',
            'type_check',
            'order',
            'status',
        )


class CheckListSzr(serializers.ModelSerializer):
    """
        Сериализатор списка чеков
    """
    class Meta:
        model = Check
        fields = (
            'uuid',
        )
