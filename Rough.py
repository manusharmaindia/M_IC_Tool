from num2words import num2words

number = 12345.67

# Converting a number to words in English
in_english = num2words(number)
print(f"Number in English: {in_english}")

# Using a different language (French)
in_french = num2words(number, to='fr')
print(f"Number in French: {in_french}")

# Specifying a custom "and" word
with_custom_and = num2words(number, andword='and')
print(f"Number with custom 'and': {with_custom_and}")

# Using a different decimal separator
with_custom_decimal = num2words(number, decimal='point')
print(f"Number with custom decimal separator: {with_custom_decimal}")

# Custom word for zero
with_custom_zero = num2words(0, zero='zero')
print(f"Zero in custom word: {with_custom_zero}")

# Specifying a custom thousands separator
with_custom_comma = num2words(1234567, comma=' ')
print(f"Number with custom comma separator: {with_custom_comma}")

# Group size (e.g., 3 for thousands, 6 for millions)
grouped_number = num2words(1234567, group=3)
print(f"Grouped number: {grouped_number}")

# Converting to currency
currency = num2words(12345.67, to_currency=True)
print(f"Currency representation: {currency}")

# Custom word for cents
with_custom_cents = num2words(0.67, to_currency=True, cents='cents')
print(f"Cents in custom word: {with_custom_cents}")

# Using "and" for cents
with_and_for_cents = num2words(0.67, to_currency=True, andcents=True)
print(f"Using 'and' for cents: {with_and_for_cents}")

# Custom word for pennies (smallest fractional unit)
with_custom_pennies = num2words(0.01, to_currency=True, pennies='pennies')
print(f"Pennies in custom word: {with_custom_pennies}")
