m = n = 4

for i in range(0, 7):
    for j in range(0, 9):

        if j == m or j == n or (i == 3 and j >= m and j <= n):
            print("*", end=" ")
        else:
            print(" ", end=" ")

    print()

    m = m - 1
    n = n + 1