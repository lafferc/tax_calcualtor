from utils import load_tax_data, calc_tax_from_bands

g_tax_data = load_tax_data()
current_year = "2018"


class Employee(object):
    tax_calculated = False
    def __init__(self, income, contribution, tax_info):
        self.anual_income = income
        self.pension = contribution * 12
        self.tax_info = tax_info
        self.tax_credits = self.tax_info["paye"]["tax_credit"]["employee"]
        self.tax_credits += self.tax_info["paye"]["tax_credit"]["single"]

    def calc_tax_bill(self):
        paye_bands = self.tax_info["paye"]["bands"]
        self.paye = calc_tax_from_bands(self.anual_income - self.pension, paye_bands)
        self.paye -= self.tax_credits

        usc_bands = self.tax_info["usc"]["bands"]
        self.usc = calc_tax_from_bands(self.anual_income, usc_bands)

        prsi_bands = self.tax_info["prsi"]["bands"]
        self.prsi = calc_tax_from_bands(self.anual_income, prsi_bands)

        self.tax_calculated = True

        return self.paye + self.usc + self.prsi

    def net_monthly_income(self):
        gross_income = self.anual_income - self.pension
        net_income = gross_income - self.calc_tax_bill()
        return net_income / 12

    def show_break_down(self):
        if not self.tax_calculated:
            self.calc_tax_bill()

        return "paye:%.2f , usc:%.2f, prsi:%.2f" % (self.paye, self.usc, self.prsi)


def tests():
    def test_equal(val, expected, places=None):
        if places is not None:
            val = round(val, places)
        assert val == expected, val

    tax_info = g_tax_data["2018"]

    e = Employee(25000, 0, tax_info)
    test_equal(e.net_monthly_income(), 1818.78, 2)

    e = Employee(50000, 0, tax_info)
    test_equal(e.net_monthly_income(), 3045.66, 2)

    e = Employee(75000, 0, tax_info)
    test_equal(e.net_monthly_income(), 4099.94, 2)

    e = Employee(100000, 0, tax_info)
    test_equal(e.net_monthly_income(), 5099.94, 2)


if __name__ == '__main__':
    import argparse
    import sys
    from tabulate import tabulate

    parser = argparse.ArgumentParser()
    parser.add_argument("salary", type=int, nargs="*")
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        tests()
        sys.exit()

    if not len(args.salary):
        salaries = [25000, 50000, 75000, 100000]
    else:
        salaries = args.salary

    monthly_pension = 0

    table = []
    for i in salaries:
        e = Employee(i, monthly_pension, g_tax_data[current_year])
        m_income = e.net_monthly_income()
        tax = i/12 - m_income
        table.append((i, m_income, 100*tax/(i/12)))

    print(tabulate(table,
                   headers=["salary", "monthly wage", "effective tax rate"],
                   floatfmt=("", ".2f", ".2f")))
