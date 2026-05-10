#include <stdio.h>

int main() {
    int i, j, k = 5;

    for(i = 1; i <= 7; i++) {

        for(j = 1; j <= 5; j++) {

            if(j == 1 || j == k)
                printf("* ");
            else
                printf("  ");
        }

        printf("\n");

        if(i < 4)
            k--;
        else
            k++;
    }

    return 0;
}