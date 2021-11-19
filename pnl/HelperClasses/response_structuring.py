from .database_operations import DatabaseOperations
import numpy as np


def fetch_category_index(entity_name, entity_category, structured_values):
    index = 0
    for key in structured_values["profitAndLoss"][entity_category]:
        if key["name"] == entity_name:
            break
        index = index + 1
    return index


class StructureResponse:

    def get_sales_evolution_monthly(self, company_id, user_id, end_index, operation_type):
        database_helper = DatabaseOperations()
        structured_values = database_helper.fetch_from_mongodb(company_id, user_id, "data")
        total_sales_index = fetch_category_index("TOTAL_SALES", "categories", structured_values)
        subcategory_list = []
        for key in structured_values["profitAndLoss"]["categories"][total_sales_index]["subCategories"]:
            subcategory_list.append(key["values"])

        monthly_tot_sales = [sum(i) for i in zip(*subcategory_list)]
        monthly_tot_sales = monthly_tot_sales[0:end_index]
        monthly_tot_sales = [int(x) for x in monthly_tot_sales]
        date_vals = structured_values["profitAndLoss"]["months"]

        return monthly_tot_sales, date_vals
    
    def sales_response_formatted(self, sales_monthly_response, date_values):
        sales_response = []

        for (sales, date) in zip(sales_monthly_response, date_values):
            response = dict()
            response["date"] = date
            response["value"] = sales
            sales_response.append(response)

        return sales_response

    def sales_response_formatted(self, sales_monthly_response, date_values):
        sales_response = []

        for (sales, date) in zip(sales_monthly_response, date_values):
            response = dict()
            response["date"] = date
            response["value"] = sales
            sales_response.append(response)

        return sales_response

    def get_category_monthly_values(self, company_id, user_id, total_sales_monthly, date_values, category_name, end_index,
                                    operation_type):
        database_helper = DatabaseOperations()
        structured_values = database_helper.fetch_from_mongodb(company_id, user_id, "data")
        index = fetch_category_index(category_name, "categories", structured_values)
        subcategory_list = []
        for key in structured_values["profitAndLoss"]["categories"][index]["subCategories"]:
            subcategory_list.append(key["values"])

        sum_of_values = [sum(i) for i in zip(*subcategory_list)]
        sum_of_values = sum_of_values[0:end_index]
        sum_of_values = [int(x) for x in sum_of_values]

        value_to_percentage_total_sales = self.get_percentage_as_total_sales(sum_of_values, total_sales_monthly)
        return self.create_listOf_dictionaries(sum_of_values, value_to_percentage_total_sales, date_values)

    def get_percentage_as_total_sales(self, monthly_values, sales_monthly_values):
        percentage_values = []
        for (value, total_sales) in zip(monthly_values, sales_monthly_values):
            percentage_values.append((value/total_sales) * 100)
        return percentage_values

    def create_listOf_dictionaries(self, monthly_values, percentage_values, date_values):

        format_response = []

        for (value, val_percentage, date) in zip(monthly_values, percentage_values, date_values):
            response = dict()
            response["date"] = date
            response["value"] = value
            response["percentage"] = val_percentage
            format_response.append(response)

        return format_response

    def get_derived_category_value(self, company_identifier, user_id, category_name, operation_type):
        database_helper = DatabaseOperations()
        structured_values = database_helper.fetch_from_mongodb(company_identifier, user_id, "data")
        index = fetch_category_index(category_name, "derivedCategories", structured_values)
        value = structured_values["profitAndLoss"]["derivedCategories"][index]["values"]
        return value

    def get_derived_category_formatted(self, monthly_value, sales_monthly_value, date_values):
        percentage_values = []
        for (gross, total_sales) in zip(monthly_value, sales_monthly_value):
            percentage_values.append((gross/total_sales) * 100)

        return self.create_listOf_dictionaries(monthly_value, percentage_values, date_values)

    def get_sales_evolution_ytd(self, comp_ID, user_id, end_index, operation_type):
        database_helper = DatabaseOperations()
        structured_values = database_helper.fetch_from_mongodb(comp_ID, user_id, "data")
        total_sales_index = fetch_category_index("TOTAL_SALES", "categories", structured_values)
        ltm = 12
        subcategory_list = []
        for key in structured_values["profitAndLoss"]["categories"][total_sales_index]["subCategories"]:
            subcategory_list.append(key["values"])

        monthly_tot_sales = [sum(i) for i in zip(*subcategory_list)]
        summed_monthly_total_sales = np.zeros(end_index-ltm + 1)
        for i in range(len(monthly_tot_sales)):
            if (len(summed_monthly_total_sales) - i) == 0:
                break
            summed_monthly_total_sales[i] = sum(monthly_tot_sales[i:i+ltm])

        summed_monthly_total_sales = [int(x) for x in summed_monthly_total_sales]
        date_vals = structured_values["profitAndLoss"]["months"]
        date_vals_ytd = date_vals[ltm-1:end_index]
        return summed_monthly_total_sales, date_vals_ytd

    def get_derived_category_ltm_formatted(self, monthly_value, end_index, sales_ltm_response, dates_ltm_response):
        ltm = 12
        summed_monthly_total_subcategory = np.zeros(end_index-ltm + 1)
        for i in range(len(monthly_value)):
            if (len(monthly_value) - (i+ltm) + 1) == 0:
                break
            summed_monthly_total_subcategory[i] = sum(monthly_value[i:i+ltm])

        summed_monthly_total_subcategory = [int(x) for x in summed_monthly_total_subcategory]
        percentage_values = []
        for (value, total_sales) in zip(summed_monthly_total_subcategory, sales_ltm_response):
            percentage_values.append((value / total_sales) * 100)

        return self.create_listOf_dictionaries(summed_monthly_total_subcategory, percentage_values, dates_ltm_response)

    def get_category_ltm_values(self, company_id, user_id, total_sales_ltm, date_values, end_index, category_name, operation_type
                                    ):
        database_helper = DatabaseOperations()
        structured_values = database_helper.fetch_from_mongodb(company_id, user_id, "data")
        index = fetch_category_index(category_name, "categories", structured_values)
        ltm = 12
        subcategory_list = []
        for key in structured_values["profitAndLoss"]["categories"][index]["subCategories"]:
            subcategory_list.append(key["values"])

        sum_of_values = [sum(i) for i in zip(*subcategory_list)]
        summed_monthly_category_total = np.zeros(end_index-ltm + 1)
        for i in range(len(sum_of_values)):
            if (len(summed_monthly_category_total) - i) == 0:
                break
            summed_monthly_category_total[i] = sum(sum_of_values[i:i+ltm])

        summed_monthly_category_total = [int(x) for x in summed_monthly_category_total]

        value_to_percentage_total_sales = self.get_percentage_as_total_sales(summed_monthly_category_total, total_sales_ltm)
        return self.create_listOf_dictionaries(summed_monthly_category_total, value_to_percentage_total_sales, date_values)


