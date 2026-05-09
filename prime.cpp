#include<iostream>
int main()
{
    int n,k=0;
    cout<<"Enter a number";
    cin>>n;
    for(int i=2; i <=n; i++)
    {
        if(n%i==0)
        {
            k++;
        }
        if(k==1)
        {
            cout<<"Prime";
        }
        else
        {
            cout<<"not prime";
        }
    }
    return 0;
}