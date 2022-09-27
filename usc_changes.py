import json

g_tax_data = None
DEFAULT_TAX_FILE = "tax_IE.json"

def load_tax_data(filename):
    global g_tax_data

    g_tax_data = json.loads(open(filename).read())

    return g_tax_data


def calc_weekly_income(year, hours):
    min_wage = g_tax_data[str(year)]["min_wage"]
    gross = min_wage * hours
    usc = calc_weekly_usc(year, gross)
    tax = calc_weekly_paye(year, gross)
    net = gross - (usc + tax)

    return year, gross, usc, net


def calc_weekly_usc(year, gross):
    return calc_usc(52, year, gross)


def calc_monthly_usc(year, gross):
    return calc_usc(12, year, gross)


def calc_usc(period, year, gross):
    usc = g_tax_data[str(year)]["usc"]

    if gross < usc["exempt"] / float(period):
        print("exempt from USC")
        return 0
    leftover = gross
    tax = 0
    for band, rate in usc["bands"]:
        if band is None or leftover < band / float(period):
            tax += leftover * rate
            return tax
        tax += (band / float(period)) * rate
        leftover = leftover - (band / float(period))
    raise RuntimeError("error in USC bands")


def calc_weekly_paye(year, gross):
    return gross * 0.2


def tests():
    def test_equal(val, expected):
        assert val == expected, val

    load_tax_data(DEFAULT_TAX_FILE)

    test_equal(calc_weekly_usc(2016, 540), 16.105)
    test_equal(calc_weekly_usc(2019, 540), 7.335)
    test_equal(calc_weekly_usc(2019, 350), 3.535)
    test_equal(calc_monthly_usc(2018, 1250), 9.985)
    test_equal(calc_weekly_income(2018, 30), (2018, 286.5, 2.265, 226.935))
    test_equal(calc_usc(1, 2017, 12000), 0)
    test_equal(calc_usc(1, 2018, 15000), 119.82)
    test_equal(calc_usc(1, 2018, 45000), 1094.26)
    test_equal(calc_usc(12, 2018, 1250), 9.985)
    test_equal(calc_usc(52, 2018, 290), 2.335)


if __name__ == "__main__":
    from tabulate import tabulate

    load_tax_data(DEFAULT_TAX_FILE)

    hours = 39
    table = []
    for year in range(2016, 2024):
        table.append(calc_weekly_income(year, hours))

    print("Weekly income of a minimum wage worker (working %d hrs per week)" % hours)
    print(tabulate(table, headers=["year", "Gross", "USC", "Net"]))

