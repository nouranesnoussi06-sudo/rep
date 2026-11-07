# LLM : problème d'associativité

- Modèle : GPT-6 
- Interface : ChatGPT
- Date : 6 novembre  2026

## Prompt
énoncé de l'exo + question : donne moi le code dans un autre language que python

## Réponse complète du LLM
1. Floating-point associativity
Comprendre le problème
En mathématiques, on sait que :
\[
(x+y)+z=x+(y+z)
\]
Mais en informatique, les nombres réels sont représentés avec une précision limitée. Les calculs peuvent donc donner des résultats différents selon l'ordre des opérations.

L'objectif est de calculer le pourcentage de fois où les deux expressions donnent exactement le même résultat.
Nos choix
Il faut préciser les choix suivants :
- Langage : C.
- Type des nombres : double (nombres flottants en double précision).
- Valeurs de x, y et z : nombres aléatoires entre -1 000 000 et 1 000 000.
- Nombre de tests : 1 000 000.
- Comparaison : égalité exacte avec ==.
- Reproductibilité : utilisation d'un générateur pseudo-aléatoire avec une graine fixe.
Programme en C
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



Comment fonctionne le programme ?
1. On génère trois nombres x, y et z.
2. On calcule (x+y)+z.
3. On calcule x+(y+z).
4. On compare les deux résultats.
5. Si les résultats sont égaux, on incrémente count.
6. À la fin, on calcule :
\[
Percentage=\frac{count}{N}\times100
\]
Reproductibilité : le générateur utilise toujours la même valeur initiale (123456789). On obtient donc la même séquence de nombres et les mêmes résultats avec la même implémentation.
## Mes commentaires

- Le LLM donne des choix clairs (double, graine fixe, comparaison exacte) mais n'annonce aucun résultat chiffré alors qu'il promet des "résultats attendus".
- Le pourcentage dépend de la distribution choisie : il tire dans [-1 000 000, 1 000 000], ce qui donne 93,06 %, contre 83,01 % pour ma version Python valeurs dans [0, 1].
- Le code compile et tourne dans Docker, avec le même résultat à chaque exécution (graine fixe).
