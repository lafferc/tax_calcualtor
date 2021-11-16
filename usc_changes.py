min_wage = {
        2016: 9.15,
        2017: 9.25,
        2018: 9.55,
        2019: 9.80,
        2020: 10.10,
        2021: 10.20,
        2022: 10.50,
    }
usc_exempt = {
        2016: 13000,
        2017: 13000,
        2018: 13000,
        2019: 13000,
        2020: 13000,
        2021: 13000,
    }
usc_bands = {
    2016: [
        (12012, 0.01),
        (6656, 0.03),
        (51376, 0.055),
        (None, 0.08)
    ],
    2017: [
        (12012, 0.005),
        (6760, 0.025),
        (51272, 0.05),
        (None, 0.08)
    ],
    2018: [
        (12012, 0.005),
        (19372, 0.02),
        (70044, 0.0475),
        (None, 0.08)
    ],
    2019: [
        (12012, 0.005),
        (19874, 0.02),
        (70044, 0.045),
        (None, 0.08)
    ],
    2020: [
        (12012, 0.005),
        (20484, 0.02),
        (70044, 0.045),
        (None, 0.08)
    ],
    2021: [
        (12012, 0.005),
        (20687, 0.02),
        (70044, 0.045),
        (None, 0.08)
    ],
}


def calc_weekly_income(year, hours):
    gross = min_wage[year] * hours
    usc = calc_weekly_usc(year, gross)
    tax = calc_weekly_paye(year, gross)
    net = gross - (usc + tax)

    return year, gross, usc, net


def calc_weekly_usc(year, gross):
    return calc_usc(52, year, gross)


def calc_monthly_usc(year, gross):
    return calc_usc(12, year, gross)


def calc_usc(period, year, gross):
    if gross < usc_exempt[year] / period:
        print("exempt from USC")
        return 0
    leftover = gross
    usc = 0
    for band, rate in usc_bands[year]:
        if band is None or leftover < band / period:
            usc += leftover * rate
            return usc
        usc += (band / period) * rate
        leftover = leftover - (band / period)
    raise RuntimeError("error in USC bands")


def calc_weekly_paye(year, gross):
    return gross * 0.2


if __name__ == "__main__":
    from tabulate import tabulate
    hours = 39
    table = []
    for year in range(2016, 2022):
        table.append(calc_weekly_income(year, hours))

    print("Weekly income of a minimum wage worker (working %d hrs per week)" % hours)
    print(tabulate(table, headers=["year", "Gross", "USC", "Net"]))
