from utils import calc_tax_from_bands

paye_bands = [
        (34550, 0.2),
        (None, 0.4)]
usc_bands = [
        (12012, 0.005),
        (19372, 0.02),
        (70044, 0.0475),
        (None, 0.08)]
prsi_bands = [
        (None, 0.04)]


class Employee(object):
    tax_calculated = False
    def __init__(self, income, contribution, tax_credits=3300):
        self.anual_income = income
        self.pension = contribution * 12
        self.tax_credits = tax_credits

    def calc_tax_bill(self):
        self.paye = calc_tax_from_bands(self.anual_income - self.pension, paye_bands)
        self.paye -= self.tax_credits

        self.usc = calc_tax_from_bands(self.anual_income, usc_bands)
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


if __name__ == '__main__':
    import argparse
    from tabulate import tabulate

    parser = argparse.ArgumentParser()
    parser.add_argument("salary", type=int, nargs="*")
    args = parser.parse_args()

    if not len(args.salary):
        salaries = [25000, 50000, 75000, 100000]
    else:
        salaries = args.salary

    table = []
    for i in salaries:
        e = Employee(i, 0)
        m_income = e.net_monthly_income()
        tax = i/12 - m_income
        table.append((i, m_income, 100*tax/(i/12)))

    print(tabulate(table,
                   headers=["salary", "monthly wage", "effective tax rate"],
                   floatfmt=("", ".2f", ".2f")))


