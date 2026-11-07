# LLM : problème de la banque

- Modèle : GPT-6 
- Interface : ChatGPT
- Date : 6 novembre  2026

## Prompt

énoncé de l'exo + question : donne moi le code dans un autre language que python


## Réponse complète du LLM

The banking problem
Comprendre le problème
Le banquier propose le fonctionnement suivant :
- On commence avec \(e \approx 2.71828\) euros.
- La première année : il prend 1 € puis multiplie le reste par 1.
- La deuxième année : il prend 1 € puis multiplie le reste par 2.
- La troisième année : il prend 1 € puis multiplie le reste par 3.
- On continue jusqu'à la 50e année.
- À la fin, il prend encore 1 € pour récupérer l'argent.
On cherche donc combien d'argent il nous reste après 50 ans.
Nos choix
Il faut préciser les hypothèses :
- Langage : C.
- Type numérique : double.
- Capital initial : 2.718281828459045.
- Durée : 50 ans.
- Frais annuels : 1 € avant chaque multiplication.
- Multiplicateur : numéro de l'année.
- Frais de retrait : 1 € supplémentaire après la 50e année.
- On suppose que le solde peut devenir négatif : aucun minimum n'est imposé.
Programme en C
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



Comprendre la formule
À chaque année \(n\), on applique :
\[
M_n=(M_{n-1}-1)\times n
\]
Avec :
\[
M_0=e
\]
Et à la fin :
\[
M_{\text{final}}=M_{50}-1
\]
Le dernier -1 correspond aux frais de retrait.
Reproductibilité
Pour vérifier que le résultat est reproductible :
1. On utilise toujours le même capital initial.
2. On utilise les mêmes opérations dans le même ordre.
3. On utilise toujours 50 années.
4. On utilise le type double.
5. On exécute plusieurs fois le programme et on compare les résultats.
Avec le même compilateur et le même environnement, on doit obtenir le même résultat.

## Mes commentaires

- Le programme calcule en double et le résultat final, environ -4,4e48 euros, est absurde. La vraie valeur est d'environ 0,02 euro (mon Python, en précision décimale, donne 0,019992165836667903...).
- Explication : l'erreur d'arrondi sur e est multipliée par n à chaque année, donc par 50! à la fin. Le montant reste correct jusqu'à l'année 16, puis diverge.
- Le LLM ne remarque pas que son résultat est faux. Sa vérification de reproductibilité (relancer le même programme) ne prouve rien : un programme déterministe donne toujours la même réponse, même fausse.
