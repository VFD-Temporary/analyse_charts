from django.shortcuts import render
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response

from .HelperClasses.database_operations import DatabaseOperations
from .HelperClasses.date_operations import DatesOperations
from .HelperClasses.response_structuring import StructureResponse
from .HelperClasses.token_operations import TokenOperation


# Create your views here.
class COSMonthlyChart(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)

        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        formatted_date = dates_helper.format_Mon_Year_to_date(date)

        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(company_identifier,
                                                                                             user_id, end_index, operation_type)
        cos_response = structuring_helper.get_category_monthly_values(company_identifier, user_id,
                                                                      sales_monthly_response,
                                                                      date_values, "COST_OF_SALES", end_index, operation_type)

        return Response(cos_response)


class GrossProfitMonthlyChart(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)

        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(company_identifier,
                                                                                             user_id, end_index,
                                                                                             operation_type)
        gross_profit_values = structuring_helper.get_derived_category_value(company_identifier, user_id, "GROSS_PROFIT",
                                                                            operation_type)
        gross_profit_values = gross_profit_values[0:end_index]
        gross_profit_values_formatted = structuring_helper.get_derived_category_formatted(gross_profit_values,
                                                                                          sales_monthly_response,
                                                                                          date_values)

        return Response(gross_profit_values_formatted)


class EBIDTAMonthly(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)

        operation_type = "profitAndLoss"
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(company_identifier,
                                                                                             user_id, end_index,
                                                                                             operation_type)
        ebidta_values = structuring_helper.get_derived_category_value(company_identifier, user_id, "EBITDA",
                                                                      operation_type)
        ebidta_values = ebidta_values[0:end_index]
        ebdita_values_formatted = structuring_helper.get_derived_category_formatted(ebidta_values,
                                                                                    sales_monthly_response, date_values)

        return Response(ebdita_values_formatted)


class SGnA(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        operation_type = "profitAndLoss"

        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )

        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(company_identifier,
                                                                                             user_id, end_index, operation_type)
        sgna_response = structuring_helper.get_category_monthly_values(company_identifier, user_id,
                                                                       sales_monthly_response,
                                                                       date_values, "TOTAL_SG_AND_A", end_index, operation_type)

        return Response(sgna_response)


class NetIncomeEvolution(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(company_identifier,
                                                                                             user_id, end_index,
                                                                                             operation_type)
        net_income_value = structuring_helper.get_derived_category_value(company_identifier, user_id, "NET_INCOME",
                                                                         operation_type)
        net_income_value = net_income_value[0:end_index]
        net_income_value_formatted = structuring_helper.get_derived_category_formatted(net_income_value,
                                                                                       sales_monthly_response,
                                                                                       date_values)
        return Response(net_income_value_formatted)

class SalesMonthlyChart(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        #user_id = "618e3d4d666df6372f59e0ad"

        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )

        sales_monthly_response, date_values = structuring_helper.get_sales_evolution_monthly(company_identifier,
                                                                                             user_id, end_index,
                                                                                             operation_type)
        sales_monthly_response_formatted = structuring_helper.sales_response_formatted(sales_monthly_response,
                                                                                       date_values)
        return Response(sales_monthly_response_formatted)



class LTMSalesChart(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        #user_id = "618e3d4d666df6372f59e0ad"
        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        formatted_date = dates_helper.format_Mon_Year_to_date(date)

        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )

        sales_ytd_response, dates_ytd_response = structuring_helper.get_sales_evolution_ytd(company_identifier,
                                                                                            user_id, end_index,
                                                                                            operation_type)
        sales_ytd_response_formatted = structuring_helper.sales_response_formatted(sales_ytd_response,
                                                                                   dates_ytd_response)

        return Response(sales_ytd_response_formatted)


class LTMEBITDA(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        #user_id = "618e3d4d666df6372f59e0ad"
        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        print("The date being sent is ", date)
        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        print("The date sent back ", formatted_date)

        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )
        sales_ltm_response, dates_ltm_response = structuring_helper.get_sales_evolution_ytd(company_identifier,
                                                                                            user_id,
                                                                                            end_index,
                                                                                            operation_type)
        ebidta_values = structuring_helper.get_derived_category_value(company_identifier, user_id, "EBITDA",
                                                                      operation_type)
        ebidta_values = ebidta_values[0:end_index]
        ebdita_values_formatted = structuring_helper.get_derived_category_ltm_formatted(ebidta_values, end_index,
                                                                                        sales_ltm_response,
                                                                                        dates_ltm_response)

        return Response(ebdita_values_formatted)


class LTMCOS(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        #user_id = "618e3d4d666df6372f59e0ad"
        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        print("The date being sent is ", date)
        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        print("The date sent back ", formatted_date)

        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )
        sales_ltm_response, dates_ltm_response = structuring_helper.get_sales_evolution_ytd(company_identifier,
                                                                                            user_id,
                                                                                            end_index,
                                                                                            operation_type)
        cos_response = structuring_helper.get_category_ltm_values(company_identifier, user_id,
                                                                  sales_ltm_response,
                                                                  dates_ltm_response, end_index, "COST_OF_SALES",
                                                                  operation_type)

        return Response(cos_response)

class LTMGrossProfit(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        #user_id = "618e3d4d666df6372f59e0ad"
        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        print("The date being sent is ", date)
        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        print("The date sent back ", formatted_date)

        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )
        sales_ltm_response, dates_ltm_response = structuring_helper.get_sales_evolution_ytd(company_identifier,
                                                                                            user_id,
                                                                                            end_index,
                                                                                            operation_type)
        gross_profit_values = structuring_helper.get_derived_category_value(company_identifier, user_id, "GROSS_PROFIT",
                                                                            operation_type)
        gross_profit_values = gross_profit_values[0:end_index]
        gross_profit_values_formatted = structuring_helper.get_derived_category_ltm_formatted(gross_profit_values, end_index,
                                                                                        sales_ltm_response,
                                                                                        dates_ltm_response)

        return Response(gross_profit_values_formatted)

class LTMNetIncome(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        #user_id = "618e3d4d666df6372f59e0ad"
        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        print("The date being sent is ", date)
        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        print("The date sent back ", formatted_date)

        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )
        sales_ltm_response, dates_ltm_response = structuring_helper.get_sales_evolution_ytd(company_identifier,
                                                                                            user_id,
                                                                                            end_index,
                                                                                            operation_type)
        net_income_values = structuring_helper.get_derived_category_value(company_identifier, user_id, "NET_INCOME",
                                                                          operation_type)
        net_income_values = net_income_values[0:end_index]
        net_income_values_formatted = structuring_helper.get_derived_category_ltm_formatted(net_income_values, end_index,
                                                                                        sales_ltm_response,
                                                                                        dates_ltm_response)

        return Response(net_income_values_formatted)

class LTMSGnA(APIView):
    permission_classes = [BasePermission]

    def get(self, request, company_identifier, date):
        # helper classes objects
        structuring_helper = StructureResponse()
        database_helper = DatabaseOperations()
        dates_helper = DatesOperations()

        token_helper = TokenOperation()
        login_token = request.COOKIES.get('LOGIN_SESSION')
        user_id = token_helper.get_user_id(login_token)
        #user_id = "618e3d4d666df6372f59e0ad"
        operation_type = "profitAndLoss"
        print("The company identifier that is sent", company_identifier)
        # check if the company is deleted (disconnected)
        is_disconnected = database_helper.check_disconnected_field(company_identifier, user_id)
        if is_disconnected:
            user_message = {"Message": "The company does not exist in the database"}
            return Response(user_message)

        print("The date being sent is ", date)
        formatted_date = dates_helper.format_Mon_Year_to_date(date)
        print("The date sent back ", formatted_date)

        end_index = dates_helper.get_end_index(
            company_identifier, user_id, operation_type, formatted_date
        )
        sales_ltm_response, dates_ltm_response = structuring_helper.get_sales_evolution_ytd(company_identifier,
                                                                                            user_id,
                                                                                            end_index,
                                                                                            operation_type)
        sgna_response = structuring_helper.get_category_ltm_values(company_identifier, user_id,
                                                                   sales_ltm_response,
                                                                   dates_ltm_response, end_index, "TOTAL_SG_AND_A",
                                                                   operation_type)

        return Response(sgna_response)