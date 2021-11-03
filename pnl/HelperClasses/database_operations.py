from pnl.models import Company
from pnl.custom_exceptions import NotInDatabaseException,DatabaseLookupError


class DatabaseOperations:

    def fetch_from_mongodb(self, companyID, userID, field_name):
        """Returns the requested data field from mongoDB for the specified companyID"""
        company_object = self.find_object_index(companyID, userID)
        if company_object is None:
            # companyID is not present in the database
            raise NotInDatabaseException("Company ID is not present in the database. ")
        try:
            # we have the index of entry with desired companyID and UserID
            field_object = Company._meta.get_field(field_name)
            field_value = field_object.value_from_object(company_object)
            return field_value
        except Exception as e:
            raise NotInDatabaseException("The specified field is not present in the database. ", str(e))

    def check_disconnected_field(self, companyID, userID):
        """Checks if the company has been disconnected (deleted) from the database"""
        field_value = False
        try:
            # checking whether the company in the database associted with
            field_value = self.fetch_from_mongodb(companyID, userID, "disconnected")
        except:
            """Ideally, the data companies that have been deleted (and hence have no data) 
            should have a field named 'disconnected' with the value 'True'. However, this isn't 
            always the case. Some deleted companies with no data do not have this field. Therefore,
            this method checks if a 'disconnected' field exists. If it does, then its value
            is read and is used for determining whether to report this as a disconnected/deleted
            company or not."""
            # not raising an exception since this is more of a database structure problem and not really an error
            pass

        if field_value == False:
            # either the column does not exist or its value is false
            return False
        elif field_value == True:
            # the database is disconnected
            return True

    def find_object_index(self, company_id_of_interest, user_id_of_interest):
        """Loops over all the objects in the database to determine the one
        associated with the "companyId" for which the data has to be extracted"""
        try:
            all_objects = Company.objects.all()
            # https://stackoverflow.com/a/51905746
            for obj in all_objects:
                userId_object = Company._meta.get_field("userId")
                companyId_object = Company._meta.get_field("companyId")
                companyId_value = companyId_object.value_from_object(obj)
                userId_value = userId_object.value_from_object(obj)
                if companyId_value == company_id_of_interest and userId_value==user_id_of_interest:
                    # this object is associated with the specified companyId (from front end)
                    # and userId (fetched from browser session cookie)
                    return obj
            return None
        except Exception as e:
            raise DatabaseLookupError("Error occured while trying to fetch values from the database. ", str(e))