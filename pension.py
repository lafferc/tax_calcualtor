import random

from utils import calc_tax_from_bands

g_retirement_age = 66
g_yearly_fee = 0.01
g_growth_range = (-2, 7)


class Pension(object):
    investment_rate = 0.95
    def __init__(self, contribution, inital_fund=0):
        self.total_contribution = inital_fund
        self._contribution = contribution
        self.fund = inital_fund

    def calc_year(self):
        for i in range(12):
            self.fund *= (1 + self.get_growth())
            self.fund += self._contribution * self.investment_rate
            self.total_contribution += self._contribution
        self.fund *= (1 - g_yearly_fee)

    def get_growth(self):
        return (random.randrange(*g_growth_range)/1200)

    def lump_sum(self):
        tax_bands = [(200000, 0),
                     (500000, 0.2),
                     (None, 0.4)]
        tax = calc_tax_from_bands(self.fund, tax_bands)
        return self.fund - tax


if __name__ == '__main__':
    import argparse

    random.seed()

    parser = argparse.ArgumentParser()
    parser.add_argument("age", type=int)
    parser.add_argument("contribution", type=float)
    args = parser.parse_args()

    curr_age = args.age
    p = Pension(args.contribution)
    for i in range(g_retirement_age - curr_age):
        p.calc_year()
        print(p.fund)
    print("fund:%d, total controbution:%d, lump sum:%d, growth:%.2f%%"
          % (p.fund, p.total_contribution, p.lump_sum(),
             ((p.lump_sum() - p.total_contribution)*100/p.lump_sum())))

