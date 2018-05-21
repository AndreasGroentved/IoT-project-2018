f = 2.3333333333333333344234323523352532

a = "%.1f" % round(f, 1)

print(a)

lightList = [2.234342432234243234423, 4.342342233243523255, 33.3423232324432432324]

lightString = '[' + ', '.join('"{0}"'.format("%.1f" % round(w, 1)) for w in lightList) + ']'
print(lightString)

print(str("123456789abcdef")[3:-3])

bbb = [15200000521, 111222333, 444555666]


def removeFirstAndLastThree(aaa):
    return str(aaa)[3:-3]


print(str(map(removeFirstAndLastThree, bbb)))
