from django.shortcuts import render
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response

from .HelperClasses.database_operations import DatabaseOperations
from .HelperClasses.response_structuring import StructureResponse
from .HelperClasses.token_operations import TokenOperation


# Create your views here.
class COSMonthlyChart(APIView):
    permission_classes = [BasePermission]

    def get(self, request, comp_ID):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)

        operation_type = "profitAndLoss"
        print("The company identifier that is sent", comp_ID)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(comp_ID, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(comp_ID,
                                                                                             user_id, operation_type)
        cos_response = structuring_helper.get_category_monthly_values(comp_ID, user_id,
                                                                      sales_monthly_response,
                                                                      date_values, "COST_OF_SALES", operation_type)

        return Response(cos_response)


class SalesMonthlyChart(APIView):
    permission_classes = [BasePermission]

    def get(self, request, comp_ID):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)

        operation_type = "profitAndLoss"
        print("The company identifier that is sent", comp_ID)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(comp_ID, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(comp_ID,
                                                                                             user_id,
                                                                                             operation_type)
        sales_monthly_response_formatted = structuring_helper.sales_response_formatted(sales_monthly_response,
                                                                                       date_values)
        return Response(sales_monthly_response_formatted)


class GrossProfitMonthlyChart(APIView):
    permission_classes = [BasePermission]

    def get(self, request, comp_ID):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)

        operation_type = "profitAndLoss"
        print("The company identifier that is sent", comp_ID)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(comp_ID, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(comp_ID,
                                                                                             user_id,
                                                                                             operation_type)
        gross_profit_values = structuring_helper.get_derived_category_value(comp_ID, user_id, "GROSS_PROFIT",
                                                                            operation_type)
        gross_profit_values_formatted = structuring_helper.get_derived_category_formatted(gross_profit_values,
                                                                                          sales_monthly_response,
                                                                                          date_values)

        return Response(gross_profit_values_formatted)


class EBIDTAMonthly(APIView):
    permission_classes = [BasePermission]

    def get(self, request, comp_ID):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)

        operation_type = "profitAndLoss"
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(comp_ID, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(comp_ID,
                                                                                             user_id,
                                                                                             operation_type)
        ebidta_values = structuring_helper.get_derived_category_value(comp_ID, user_id, "EBITDA",
                                                                      operation_type)
        ebdita_values_formatted = structuring_helper.get_derived_category_formatted(ebidta_values,
                                                                                    sales_monthly_response, date_values)

        return Response(ebdita_values_formatted)


class SGnA(APIView):
    permission_classes = [BasePermission]

    def get(self, request, comp_ID):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        operation_type = "profitAndLoss"

        print("The company identifier that is sent", comp_ID)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(comp_ID, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(comp_ID,
                                                                                             user_id, operation_type)
        sgna_response = structuring_helper.get_category_monthly_values(comp_ID, user_id,
                                                                       sales_monthly_response,
                                                                       date_values, "TOTAL_SG_AND_A", operation_type)

        return Response(sgna_response)


class NetIncomeEvolution(APIView):
    permission_classes = [BasePermission]

    def get(self, request, comp_ID):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        operation_type = "profitAndLoss"
        print("The company identifier that is sent", comp_ID)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(comp_ID, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(comp_ID,
                                                                                             user_id,
                                                                                             operation_type)
        net_income_value = structuring_helper.get_derived_category_value(comp_ID, user_id, "NET_INCOME",
                                                                         operation_type)

        net_income_value_formatted = structuring_helper.get_derived_category_formatted(net_income_value,
                                                                                       sales_monthly_response,
                                                                                       date_values)
        return Response(net_income_value_formatted)
