#include<stdio.h>
int main(){
    int i, j, size, m=0, n=5;
    printf("Enter size");
    scanf("%d", &size);
    for(i=0;i<=size;i++)
    {
        for(j=0;j<=size-1;j++)
        {
            if(j==1 || (i==j+1 && j!=0))
            {
                printf("*");
            }
            else if(i==m && j==n)
            {
                printf("* ");
                m=m+1;
                n=n-1;
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }
    return 0;
}