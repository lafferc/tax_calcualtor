from income_tax import Employee

def mortgage_value_limit(income=None, deposit=None, ftb=True):
    max_value = None
    if income is not None:
        max_value = income * 3.5

    if deposit is not None:
        value = deposit * (9 if ftb else 4)
        max_value = max(max_value, value) if max_value else value

    return max_value


def deposit_needed(mortgage, ftb=True):
    return mortgage / (9 if ftb else 4)


def max_income_tax_refund(property_value):
    return min(20000, property_value * 0.05)


def calc_income_tax_refund(incomes_per_year, property_value):
    """ Calculates the amount of income tax refund
        based on the last 4 years of income
        and the value of the property."""

    total_income_tax = 0
    for income in incomes_per_year[-4:]:
        employee = Employee(income, 0)
        employee.calc_tax_bill()
        total_income_tax += employee.paye

    return min(total_income_tax, max_income_tax_refund(property_value))

