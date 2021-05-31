# Cálculo de ranura de paso fraccionado

## Parámetros
Dado un $q$ fraccional, calcula sus parámetros relacionados:

$$
q = \frac{N}{\beta} = \frac{a + b}{\beta}
$$

- Determina el grupo recurrente (unidad) en $\beta$ polos.
- Calcula 3 opciones de acortamiento de paso y sus respectivos factores de acortamiento $kp$ para la fundamental, 5ta y 7ma armónicas.
## Calculo de sucesión de ranuras
La estrella de la segunda capa consiste en sumarle a la sucesión el paso de bobina elegido (restándole $3N$ si es mayor a esa cantidad).

Ej: Si el paso de bobina seleccionado es $5$, la estrella de la segunda capa empezará en la ranura $1 + 5 = 6$. 
## Reporte

Genera un archivo de texto llamado reporte.txt y un archivo con el gráfico de la estrella de ranuras llamado slot_star.dxf


## Errores
En algunos casos el bobinado de ranura fraccionada no es realizable ya que no cumple con las condiciones de simetría.
Esto se da para $ \frac{\beta}{m}\in \Z $ , es decir $\beta$ dividido el número de fases es igual a un entero.

## Bibliografía
(A-C Machines) Michael Liwschitz-Garik - Electric Machinery. 2-D. Van Nostrand Company (1946)
