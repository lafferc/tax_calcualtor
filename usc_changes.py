min_wage = {
        2016: 9.15,
        2017: 9.25,
        2018: 9.55,
        2019: 9.80,
    }
usc_exempt = {
        2016: 13000,
        2017: 13000,
        2018: 13000,
        2019: 13000,
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
}


def calc_weekly_income(year, hours):
    gross = min_wage[year] * hours
    print year, "gross", gross
    usc = calc_weekly_usc(year, gross)
    tax = calc_weekly_paye(year, gross)
    net = gross - (usc + tax)
    print year, "Net  ", net


def calc_weekly_usc(year, gross):
    return calc_usc(52, year, gross)


def calc_monthly_usc(year, gross):
    return calc_usc(12, year, gross)


def calc_usc(period, year, gross):
    if gross < usc_exempt[year] / period:
        print "exempt from USC"
        return 0
    leftover = gross
    usc = 0
    for band, rate in usc_bands[year]:
        if band is None or leftover < band / period:
            usc += leftover * rate
            print year, "USC  ", usc
            return usc
        usc += (band / period) * rate
        leftover = leftover - (band / period)
    print "error in USC bands"


def calc_weekly_paye(year, gross):
    return gross * 0.2


if __name__ == "__main__":
    calc_weekly_income(2016, 39)
    calc_weekly_income(2017, 39)
    calc_weekly_income(2018, 39)
    calc_weekly_income(2019, 39)

