# Shiyun Liu Homework 1

P = float(input('Please enter the initial amount invested or borrowed:\n'))
r = float(input('Please enter the annual rate of interest (decimal or percent):\n'))
n = float(input('Please enter the number of times the interest rate compounds per year:\n'))
t = float(input('Please enter the term of the loan or the number of years before it is repaid:\n'))

#check whether interest rate entered in percentage or decimal
if r > 1:
    r /= 100

A = P * ((1 + r / n) ** (n * t))

print('''In {0:.0f} years, at the interest rate of {1:.0%} compounded {2:.0f} times per year,
the initial amount of ${3:,.2f} will be worth ${4:,.2f}. ${5:,.2f} will be paid in interest.'''.format(t, r, n, P, A, (A-P)))