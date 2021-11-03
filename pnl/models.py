from djongo import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


# SETTINGS FOR MODELS https://docs.djangoproject.com/en/3.2/ref/models/options/

class Subcategory(models.Model):
    class SpecialIdentifier(models.TextChoices):
        CASH = _("c")
        DEBT = _("d")
        FIXED_ASSETS = _("Fixed Assets")
        DEPRECIATION = _("Depreciation")

    # TODO: Check for methods this model might need to have
    name = models.CharField(max_length=200)
    values = models.JSONField()
    specialIdentifier = models.CharField(choices=SpecialIdentifier.choices, default=None)

    class Meta:
        abstract = True


class Month(models.Model):
    month = models.CharField(max_length=200)

    class Meta:
        abstract = True


class Category(models.Model):
    """

    TODO: Change Category and derived Category to model inheriting from super model (class - superclass). Avoid
    Code duplication
    """

    class AccountType(models.Choices):
        class ReportType(models.Choices):
            PnL = _("P&L")
            BS = _("BS")
            CF = _("CF")
            UNCLASSIFIED = _("UNCLASSIFIED")

        UNCLASSIFIED = _("Unclassified"), _(ReportType.UNCLASSIFIED)

        # PNL Categories
        TOTAL_SALES = _("Total Sales"), _(ReportType.PnL)
        COST_OF_SALES = _("Cost of Sales"), _(ReportType.PnL)
        TOTAL_SG_AND_A = _("Total SG&A"), _(ReportType.PnL)
        DEPRECIATION_AND_AMORTIZATION = _("Depreciation & Amortization"), _(ReportType.PnL)
        INTEREST_AND_OTHER_NON_OPERATIONAL = _("Interests & Other Non Operational"), _(ReportType.PnL)
        INCOME_TAXES = _("Income Taxes"), _(ReportType.PnL)
        DIVIDENDS = _("Dividends"), _(ReportType.PnL)

        # PNL Derived Categories
        GROSS_PROFIT = _("Gross Profit"), _(ReportType.PnL)
        EBITDA = _("EBITDA"), _(ReportType.PnL)
        EBIT = _("EBIT"), _(ReportType.PnL)
        EBT = _("Earnings Before Taxes"), _(ReportType.PnL)
        NET_INCOME = _("Net Income"), _(ReportType.PnL)

        # Balance Sheet Categories
        CURRENT_ASSETS = _("Total Current Assets"), _(ReportType.BS)
        NON_CURRENT_ASSETS = _("Total Non-Current Assets"), _(ReportType.BS)
        CURRENT_LIABILITIES = _("Current Liabilities"), _(ReportType.BS)
        NON_CURRENT_LIABILITIES = _("Total Non=Current Liabilities"), _(ReportType.BS)
        EQUITY = _("Total Equity"), _(ReportType.BS)

        # Balance Sheet Derived Categories
        TOTAL_ASSETS = _("Total Assets"), _(ReportType.BS)
        TOTAL_LIABILITIES = _("Total Liabilities"), _(ReportType.BS)
        TOTAL_LIABILITIES_AND_EQUITY = _("Total Liabilities and Equity"), _(ReportType.BS)

        # CashFlow Categories
        CF_OPERATIONS = _("CF From Operations"), _(ReportType.CF)
        CF_INVESTING = _("CF From Investingpyth"), _(ReportType.CF)
        CF_FINANCING = _("CF From Financing"), _(ReportType.CF)

        # CashFlow Derived
        FREE_CASHFLOW = _("Free Cash Flow"), _(ReportType.CF)
        UNIDENTIFIED_ITEMS = _("Unidentified Items"), _(ReportType.CF)
        CHANGE_IN_CASH = _("Change in Cash"), _(ReportType.CF)

    name = models.CharField(choices=AccountType.choices, default="null")

    subCategories = models.ArrayField(model_container=Subcategory)

    class Meta:
        abstract = True


class DerivedCategory(models.Model):
    class AccountType(models.Choices):
        class ReportType(models.Choices):
            PnL = _("P&L")
            BS = _("BS")
            CF = _("CF")
            UNCLASSIFIED = _("UNCLASSIFIED")

        UNCLASSIFIED = _("Unclassified"), _(ReportType.UNCLASSIFIED)

        # PNL Categories
        TOTAL_SALES = _("Total Sales"), _(ReportType.PnL)
        COST_OF_SALES = _("Cost of Sales"), _(ReportType.PnL)
        TOTAL_SG_AND_A = _("Total SG&A"), _(ReportType.PnL)
        DEPRECIATION_AND_AMORTIZATION = _("Depreciation & Amortization"), _(ReportType.PnL)
        INTEREST_AND_OTHER_NON_OPERATIONAL = _("Interests & Other Non Operational"), _(ReportType.PnL)
        INCOME_TAXES = _("Income Taxes"), _(ReportType.PnL)
        DIVIDENDS = _("Dividends"), _(ReportType.PnL)

        # PNL Derived Categories
        GROSS_PROFIT = _("Gross Profit"), _(ReportType.PnL)
        EBITDA = _("EBITDA"), _(ReportType.PnL)
        EBIT = _("EBIT"), _(ReportType.PnL)
        EBT = _("Earnings Before Taxes"), _(ReportType.PnL)
        NET_INCOME = _("Net Income"), _(ReportType.PnL)

        # Balance Sheet Categories
        CURRENT_ASSETS = _("Total Current Assets"), _(ReportType.BS)
        NON_CURRENT_ASSETS = _("Total Non-Current Assets"), _(ReportType.BS)
        CURRENT_LIABILITIES = _("Current Liabilities"), _(ReportType.BS)
        NON_CURRENT_LIABILITIES = _("Total Non=Current Liabilities"), _(ReportType.BS)
        EQUITY = _("Total Equity"), _(ReportType.BS)

        # Balance Sheet Derived Categories
        TOTAL_ASSETS = _("Total Assets"), _(ReportType.BS)
        TOTAL_LIABILITIES = _("Total Liabilities"), _(ReportType.BS)
        TOTAL_LIABILITIES_AND_EQUITY = _("Total Liabilities and Equity"), _(ReportType.BS)

        # CashFlow Categories
        CF_OPERATIONS = _("CF From Operations"), _(ReportType.CF)
        CF_INVESTING = _("CF From Investingpyth"), _(ReportType.CF)
        CF_FINANCING = _("CF From Financing"), _(ReportType.CF)

        # CashFlow Derived
        FREE_CASHFLOW = _("Free Cash Flow"), _(ReportType.CF)
        UNIDENTIFIED_ITEMS = _("Unidentified Items"), _(ReportType.CF)
        CHANGE_IN_CASH = _("Change in Cash"), _(ReportType.CF)

    name = models.CharField(choices=AccountType.choices, default="null")
    values = models.JSONField()

    class Meta:
        abstract = True


class CompanyData(models.Model):
    class PNL(models.Model):
        name_of_field = models.EmbeddedField(Category)
        value = models.ArrayField(Subcategory)

        class Meta:
            abstract = True

    """
    To keep the appropriate djongo Django to Model translation (in which the variable name gets used as
    document name in mongo, exec was used below to generate that variable name from string.

    THIS IS HORRENDOUS PRACTICE. IT IS ALSO THE WORST IDEA EVER TO LEAVE LONG-TERM. BUT IT WORKS NOW, OKAY? CHANGE LATER
    Move this practice to an array that generates the name based on string directly.
    This will change the MongoDB structure, but it will be changed regardless once the migration is done.

    Alternative patch-up until migration is done:
        name  = 'varname'
        value = 'something'
        setattr(self, name, value) #equivalent to: self.varname= 'something'
        print (self.varname)
        #will print 'something'


    foo = "bar"
    exec(foo + " = 'something else'")
    print bar

    """
    _id = models.ObjectIdField()
    profitAndLoss = models.EmbeddedField(PNL)
    balanceSheet = models.CharField(max_length=200)

    class Meta:
        abstract = True


class TimeSeries(models.Model):
    months = models.JSONField()
    categories = models.ArrayField(model_container=Category)  # make Category Model
    derivedCategories = models.ArrayField(model_container=DerivedCategory)  # make derivedCategories Model

    class Meta:
        abstract = True


class QoKoonDate(models.Model):
    date = models.CharField(max_length=200)

    class Meta:
        abstract = True


class CompanyMeta(models.Model):
    updatedOn = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)
    financialYearStartMonth = models.IntegerField()
    financialYearStartDay = models.IntegerField()

    class Meta:
        abstract = True


class QokoonInput(models.Model):
    # id = models.CharField(max_length=200, primary_key=True)
    # profitAndLoss = models.CharField(max_length=200)
    profitAndLoss = models.EmbeddedField(model_container=TimeSeries)
    balanceSheet = models.EmbeddedField(model_container=TimeSeries)
    cashflow = models.EmbeddedField(model_container=TimeSeries)

    class Meta:
        abstract = True


class COACommonDBModel(models.Model):
    id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    specialIdentifier = models.CharField(max_length=200)

    class Meta:
        abstract = True


class ProfitAndLoss(models.Model):
    totalSales = models.ArrayField(model_container=COACommonDBModel)  # make Chart Of Accounts common DB model
    costOfSales = models.ArrayField(model_container=COACommonDBModel)
    totalSGAndA = models.ArrayField(model_container=COACommonDBModel)
    depreciationAndAmortization = models.ArrayField(model_container=COACommonDBModel)
    interestAndOtherNonOperational = models.ArrayField(model_container=COACommonDBModel)
    incomeTaxes = models.ArrayField(model_container=COACommonDBModel)
    dividends = models.ArrayField(model_container=COACommonDBModel)

    class Meta:
        abstract = True


class BalanceSheet(models.Model):
    nonCurrentAssets = models.ArrayField(model_container=COACommonDBModel)  # make Chart Of Accounts common DB model
    nonCurrentLiabilities = models.ArrayField(model_container=COACommonDBModel)
    equity = models.ArrayField(model_container=COACommonDBModel)
    currentAssets = models.ArrayField(model_container=COACommonDBModel)
    currentLiabilities = models.ArrayField(model_container=COACommonDBModel)

    class Meta:
        abstract = True


class ChartOfAccounts(models.Model):
    userId = models.CharField(max_length=200)
    companyId = models.CharField(max_length=200)
    profitAndLoss = models.EmbeddedField(
        model_container=ProfitAndLoss)  # make Profit and Loss model in Chart of Account
    balanceSheet = models.EmbeddedField(model_container=BalanceSheet)  # make BalanceSheet model in Chart of Account

    class Meta:
        abstract = True


class ChartOfAccountsDefault(models.Model):
    userId = models.CharField(max_length=200)
    companyId = models.CharField(max_length=200)
    profitAndLoss = models.EmbeddedField(
        model_container=ProfitAndLoss)  # make Profit and Loss model in Chart of Account
    balanceSheet = models.EmbeddedField(model_container=BalanceSheet)  # make BalanceSheet model in Chart of Account

    class Meta:
        abstract = True
        # managed = False !! is this a potential fix??????


class Company(models.Model):
    """
    something = Company(userId=data[0]['userId'], companyId=data[0]['companyId'], companyName=data[0]['companyName'],
    data=data[0]['data'],meta=data[0]['meta'])

    """
    userId = models.CharField(max_length=200)
    companyId = models.CharField(max_length=200)
    companyName = models.CharField(max_length=200)
    data = models.EmbeddedField(model_container=QokoonInput)
    meta = models.EmbeddedField(model_container=CompanyMeta)

    class Meta:
        db_table = "company"


class TokenClass(models.Model):
    refreshToken = models.CharField(max_length=300)
    accessToken = models.CharField(max_length=300)

    class Meta:
        abstract = True


class Companies(models.Model):

    class Meta:
        abstract = True


"""

instance = class(paramets=value).save()
"""