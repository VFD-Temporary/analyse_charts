from .database_operations import DatabaseOperations
from pnl.custom_exceptions import NoDataException, DataFieldNotPresent, UnExpexpectedDurationError, \
    InvalidDatesException, IncorrectSlicingError, DateTypeCastingError


class DatesOperations:

    def is_leap(self, year):
        """Checks if a year (YY) is a leap year"""
        try:
            year = float(year)
        except TypeError as e:
            raise DateTypeCastingError("A non numeric value encountered for 'year'. ", str(e))
        except ValueError as e:
            raise DateTypeCastingError("A non numeric value encountered for 'year'. ", str(e))
        if year % 4 == 0:
            return True
        else:
            return False

    def format_Mon_Year_to_date(self, date):
        """Changes the date from 'MMM-YYYY' to 'MM' """
        MM_to_DD_MMM = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
                        "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        return str(MM_to_DD_MMM[date[0:3]] + " " + date[4:])

    def format_MMYY_to_date(self, date):
        """Changes the date from 'MM-YY' to 'DD MMM YY' """
        MM_to_DD_MMM = {"01": "31 Jan", "03": "31 Mar", "04": "30 Apr",
                        "05": "31 May", "06": "30 Jun", "07": "31 Jul", "08": "31 Aug", "09": "30 Sep",
                        "10": "31 Oct", "11": "30 Nov", "12": "31 Dec"}
        try:
            if int(date[0:2]) == 2 and self.is_leap(int(date[3:])):
                return "29 Feb" + " " + date[3:]
            elif int(date[0:2]) == 2 and not self.is_leap(int(date[3:])):
                return "28 Feb" + " " + date[3:]
            else:
                formatted_date = str(MM_to_DD_MMM[date[0:2]] + " " + date[3:])
                # 01-20 converted to 31-Jan-2020
            return formatted_date
        except TypeError as e:
            raise DateTypeCastingError("An error occured while converting dates to 'DD Mon YY' format. ", str(e))

    def get_end_index(self, company_id, user_id, operation_type, selected_date):
        database_helper = DatabaseOperations()
        # extracting months field from the db
        data = database_helper.fetch_from_mongodb(company_id, user_id, "data")
        data_field = data[operation_type]

        try:
            months = data_field["months"]
            if len(months) == 0:
                raise NoDataException("The database does not contain any data")
        except Exception as e:
            raise DataFieldNotPresent("The database has no field 'months'. ", str(e))

        formatted_ending_date = self.format_MMYY_to_date(selected_date)
        formatted_ending_date_YYYY = formatted_ending_date[0:7] + "20" + formatted_ending_date[7:]

        try:
            end_date_index = months.index(formatted_ending_date)
        except:
            end_date_index = months.index(formatted_ending_date_YYYY)

        return end_date_index + 1
