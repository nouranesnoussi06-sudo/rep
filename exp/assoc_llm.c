#include <stdio.h>
#include <stdint.h>

static uint64_t state;

static uint64_t next_u64(void) {
    state ^= state << 13;
    state ^= state >> 7;
    state ^= state << 17;
    return state;
}

static double next_double(double low, double high) {
    return ((next_u64() >> 11) / 9007199254740992.0) * (high - low) + low;
}

int main(int argc, char **argv) {
    unsigned long long repetitions = 1000000ULL, seed = 123456789ULL;
    double low = -1000000.0, high = 1000000.0;
    for (int i = 1; i < argc; i++) {
        sscanf(argv[i], "--repetitions=%llu", &repetitions);
        sscanf(argv[i], "--seed=%llu", &seed);
        sscanf(argv[i], "--low=%lf", &low);
        sscanf(argv[i], "--high=%lf", &high);
    }
    state = seed ? seed : 88172645463325252ULL; /* xorshift cannot start from 0 */

    unsigned long long count = 0;
    for (unsigned long long i = 0; i < repetitions; i++) {
        double x = next_double(low, high);
        double y = next_double(low, high);
        double z = next_double(low, high);
        double a = (x + y) + z;
        double b = x + (y + z);
        if (a == b) count++;
    }
    printf("{\"repetitions\": %llu, \"seed\": %llu, \"low\": %g, \"high\": %g, \"percentage\": %.4f}\n",
           repetitions, seed, low, high, 100.0 * (double)count / (double)repetitions);
    return 0;
}
