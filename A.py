m = n = 4

for i in range(1, 6):
    for j in range(1, 8):

        if j == n or j == m or (i == 3 and (j >= n and j <= m)):
            print("*", end="\t")
        else:
            print(" ", end="\t")

    print()

    n -= 1
    m += 1