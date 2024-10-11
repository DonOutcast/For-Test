import csv

from django.http import HttpResponse
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, views, status
from rest_framework.response import Response

from core.api.v1.serializers import ProfileSerializer, TransactionSerializer, ReportResponseSerializer, \
    ReportRequestSerializer
from core.models import Profile, Transaction


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class FinancialReportView(views.APIView):

    @swagger_auto_schema(
        request_body=ReportRequestSerializer,
        responses={200: ReportResponseSerializer},
    )
    def post(self, request):
        serializer = ReportRequestSerializer(data=request.data)
        if serializer.is_valid():
            from datetime import datetime

            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            end_date = datetime.combine(end_date, datetime.max.time())

            total_income = Transaction.objects.filter(
                created_at__range=[start_date, end_date],
                category=Transaction.TypeOfTransaction.INCOME
            ).aggregate(total=Sum('summ'))['total'] or 0

            total_expense = Transaction.objects.filter(
                created_at__range=[start_date, end_date],
                category=Transaction.TypeOfTransaction.EXPENSE
            ).aggregate(total=Sum('summ'))['total'] or 0

            response_data = {
                'total_income': total_income,
                'total_expense': total_expense,
            }
            response_serializer = ReportResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportTransactionsCSVView(views.APIView):

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'User', 'Amount', 'Category', 'Created At'])
        transactions = Transaction.objects.all()

        for transaction in transactions:
            writer.writerow([
                transaction.id,
                transaction.user,
                transaction.summ,
                transaction.get_category_display(),
                transaction.created_at
            ])

        return response


class ExportReportCSVView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = ReportRequestSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="report_{start_date}_{end_date}.csv"'
            writer = csv.writer(response)
            writer.writerow(['User', 'Amount', 'Category', 'Date'])
            transactions = Transaction.objects.filter(created_at__range=[start_date, end_date])
            for transaction in transactions:
                writer.writerow([transaction.user, transaction.summ, transaction.category, transaction.created_at])

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
