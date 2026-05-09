#include <iostream>

int main()
{
    int i, j, m, n;

    m = n = 4;

    for (i = 1; i <= 5; i++)
    {
        for (j = 1; j <= 7; j++)
        {
            if (j == n || j == m || (i == 3 && (j >= n && j <= m)))
            {
                cout << "\t*";
            }
            else
            {
                cout << "\t ";
            }
        }

        cout << "\n";

        n--;
        m++;
    }

    return 0;
}