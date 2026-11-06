#include <stdio.h>
#include <stdint.h>

#define N 1000000

// Generateur pseudo-aleatoire reproductible
uint64_t state = 123456789;

uint64_t random_uint64() {
    state ^= state << 13;
    state ^= state >> 7;
    state ^= state << 17;
    return state;
}

double random_double() {
    return ((random_uint64() >> 11) / 9007199254740992.0)
           * 2000000.0 - 1000000.0;
}

int main() {
    int count = 0;

    for (int i = 0; i < N; i++) {
        double x = random_double();
        double y = random_double();
        double z = random_double();

        double a = (x + y) + z;
        double b = x + (y + z);

        if (a == b) {
            count++;
        }
    }

    double percentage = (double) count / N * 100;

    printf("Number of tests: %d\n", N);
    printf("Equal results: %d\n", count);
    printf("Percentage: %.2f%%\n", percentage);

    return 0;
}