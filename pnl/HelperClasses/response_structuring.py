from .database_operations import DatabaseOperations


def fetch_category_index(entity_name, entity_category, structured_values):
    index = 0
    for key in structured_values["profitAndLoss"][entity_category]:
        if key["name"] == entity_name:
            break
        index = index + 1
    return index


class StructureResponse:

    def get_sales_evolution_monthly(self, company_id, user_id, operation_type):
        database_helper = DatabaseOperations()
        structured_values = database_helper.fetch_from_mongodb(company_id, user_id, "data")
        total_sales_index = fetch_category_index("TOTAL_SALES", "categories", structured_values)
        subcategory_list = []
        for key in structured_values["profitAndLoss"]["categories"][total_sales_index]["subCategories"]:
            subcategory_list.append(key["values"])

        monthly_tot_sales = [sum(i) for i in zip(*subcategory_list)]
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

    def get_category_monthly_values(self, company_id, user_id, total_sales_monthly, date_values, category_name,
                                    operation_type):
        database_helper = DatabaseOperations()
        structured_values = database_helper.fetch_from_mongodb(company_id, user_id, "data")
        index = fetch_category_index(category_name, "categories", structured_values)
        subcategory_list = []
        for key in structured_values["profitAndLoss"]["categories"][index]["subCategories"]:
            subcategory_list.append(key["values"])

        sum_of_values = [sum(i) for i in zip(*subcategory_list)]
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
