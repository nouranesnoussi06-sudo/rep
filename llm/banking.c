#include <stdio.h>

int main() {

    double money = 2.718281828459045;

    printf("Initial amount: %.15f euros\n", money);

    for (int year = 1; year <= 50; year++) {

        // Annual fee
        money = money - 1.0;

        // Multiply by the current year
        money = money * year;

        printf("Year %d: %.15f euros\n", year, money);
    }

    // Withdrawal fee
    money = money - 1.0;

    printf("\nFinal amount: %.15f euros\n", money);

    return 0;
}