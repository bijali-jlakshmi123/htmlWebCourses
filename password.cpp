#include <iostream>
#include <string>
using namespace std;

void password(string n, int q)
{
    string k;

    cout << "Enter Password: ";
    cin >> k;

    if (k == n)
    {
        cout << "Login Successfully" << endl;
    }
    else
    {
        cout << "\nPassword try again" << endl;
        q = q + 1;

        if (q < 3)
        {
            password(n, q);
        }
        else if (q == 3)
        {
            cout << "You have entered password to max limit... Please try again" << endl;
        }
        else
        {
            cout << "Invalid input please check entered password" << endl;
        }
    }
}

int main()
{
    string n;

    cout << "Enter Password: ";
    cin >> n;

    password(n, 0);

    return 0;
}