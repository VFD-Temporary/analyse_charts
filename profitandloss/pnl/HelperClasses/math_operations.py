import numpy as np

class MathComputations:

    def get_total_category_value(self, category, p1_start_index, p1_end_index, p2_start_index, p2_end_index):
        """Calculates the total values of a BS category"""
        num_subcategories = len(category["subCategories"])
        p1_total = 0
        p2_total = 0
        for i in range(num_subcategories):
            this_subcategory = category["subCategories"][i]
            this_subcategory_p1_values = this_subcategory["values"][p1_start_index:p1_end_index]
            p1_total += np.sum(this_subcategory_p1_values)
            this_subcategory_p2_values = this_subcategory["values"][p2_start_index:p2_end_index]
            p2_total += np.sum(this_subcategory_p2_values)
        # rounding to three decimal precision
        p1_total = round(float(p1_total), 3)
        p2_total = round(float(p2_total), 3)
        return float(p1_total), float(p2_total)

    def calculate_growth_rate(self, period_1, period_2):
        """Calculates the growth rate percentage of current value wrt to previous value"""
        if period_1 == 0:
            return "N/A"
        elif period_1 > 0:
            growth_rate = (period_2 / period_1) - 1
        elif period_1 < 0:
            growth_rate = -1 * ((period_2 / period_1) - 1)
        growth_rate = growth_rate * 100
        return round(growth_rate, 3)

    def calculate_percentage(self, value, total_value):
        """Returns the percentage that 'value' is of the 'total_value' """
        if total_value==0:
            return 0
        else:
            percentage = (value * 100.00) / total_value  # computes float
            return round(percentage, 3)
     
    def get_total_section_value(self, section_name, section_data):
        """Calculates the total value of a BS section: Asset and Liability"""
        # total asset value = non current assets + current assets
        if section_name == "assets":
            # current_assets = [2], non_current = [0]
            current = section_data[2][0]["values"][0]
            non_current = section_data[0][0]["values"][0]
            p1_value = current["period1"]["value"] + non_current["period1"]["value"] 
            p2_value = current["period2"]["value"] + non_current["period2"]["value"]
            p1_percent = current["period1"]["percentage"] + non_current["period1"]["percentage"]
            p2_percent = current["period2"]["percentage"] + non_current["period2"]["percentage"]
        
        # total liability value = non current liability + current liability
        if section_name == "liabilities":
            # current_assets = [0], non_current = [2]
            current = section_data[0][0]["values"][0]
            non_current = section_data[2][0]["values"][0]
            p1_value = current["period1"]["value"] + non_current["period1"]["value"] 
            p2_value = current["period2"]["value"] + non_current["period2"]["value"]
            p1_percent = current["period1"]["percentage"] + non_current["period1"]["percentage"]
            p2_percent = current["period2"]["percentage"] + non_current["period2"]["percentage"]
        
        #rounding to three decimal places
        p1_value = round(p1_value, 3)
        p1_percent = round(p1_percent, 3)
        p2_value = round(p2_value, 3)
        p2_percent = round(p2_percent, 3)
        return (p1_value, p1_percent, p2_value, p2_percent)
