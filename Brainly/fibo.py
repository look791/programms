# Dane
n = 20
m = n
x = 6
print("Ilość wyrazów ciągu: " + str(n))
print("Dana: " + str(x))
# Zmienne
a = 0
b = 1
c = 1
F = [a, b, c]
R = []
# Ciąg Fibo
while n > 0:
    F.append(F[-2] + F[-1])
    n = n - 1
print("Ciąg Fibonacciego: ")
print(F)

# Liczby pierwsze
P = [x for x in range(2, max(F)) if all(x % y for y in range(2, x))]
print("Liczby pierwsze: ")
print(P)

# Algorytm
for f in F:
    if f >= x:
        R.append(f)
for r in R:
    for p in P:
        if r == p:
            R.remove(r)
print("Liczby większe lub równe od " + str(x) + " będące liczbami ciągu Fibonacciego ale nie bedące liczbami pierwszymi: ")
print(R)
