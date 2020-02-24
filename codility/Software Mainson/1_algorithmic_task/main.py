A = [2, 3, 9, 2, 5, 1, 3, 7, 10]
B = [2, 1, 3, 4, 3, 10, 6, 6, 1, 7, 10, 10, 10]
C = []
D = []
P = [i for i in range(2,len(B)) if all(i%j for j in range(2,i))]
N = [i for i in range(len(B))]
S = [i for i in N if all(i != j for j in P)]

print("A = " + str(A))
print("B = " + str(B))

i = 0
j = 0
D = [a*0 for a in range(len(A))]
E = []
for a in A:
    while i <= (len(B) - 1):
        if B[i] == a:
           D[j] = D[j] + 1
        i = i + 1
    i = 0
    j = j + 1
i = 0
j = 0
for d in D:
    while i <= (len(P) - 1):
        if d == S[i]:
             C.append(A[j])
        i = i + 1
    j = j + 1
    i = 0
print("C = " + str(C))





