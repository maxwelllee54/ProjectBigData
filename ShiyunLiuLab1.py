# Shiyun Liu Lab 1

billAmount = float(input('Please enter the billed amount:\n'))
tipPercent = float(input('Please enter your desired tip as decimal:\n'))

tip = billAmount * tipPercent

billTotal = billAmount + tip

print(tipPercent*100, 'percent of $', billAmount, 'is $', tip)
print('Your total bill amount is: $', billTotal)