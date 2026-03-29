```C
#include <stdio.h>
int main (){ 
int ninicial,nfinal,nincremento,i; //Declaracion de variables
//Se pide los datos al usuario
printf ("Ingrese el numero inicial:");
scanf ("%d", &ninicial);
printf ("Ingrese el numero final:");
scanf ("%d", &nfinal);
printf ("Ingrese el valor de incremento:");
scanf ("%d", &nincremento);

// 1 validacion: el valor de incremento no puede ser cero
if (nincremento==0){
    printf ("El valor de incremento no puede ser 0");
    return 1; // Termina con error el programa
}

// 2 validacion: el valor de incremento debe ser positivo
if(nincremento<0){
    printf ("El valor del incremento debe ser positivo");
    return 1; // Termina con error el programa
}

// 3 validacion: el valor inicial debe ser menor que el valor final
if(ninicial>nfinal){
    printf ("El valor inicial debe ser menor que el final");
    return 1; // Termina con error el programa
}

/*En este ciclo repetitivo for recorremos desde inicio hasta fin, saltaando de incremento en incremento
i = ninicial: Indicamos que  el contador arranca en el numero inicial dado por el usuario
i <= nfinal: Indicamos el numero al que vamos a llegar
i = i+ nincremento: Indicamos el numero de incremento
*/
for (i= ninicial; i<=nfinal; i= i+ nincremento){
    printf ("%d\n", i); // Imprime el resultado
}
return 0;

}
```
Camilo es tonto
