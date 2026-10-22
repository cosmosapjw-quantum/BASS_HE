#ifndef HE35_PAIR_H
#define HE35_PAIR_H
/* Row-major thermal and STF matrices [A,B]; rates ascending, s^-1.
   kappa m^3/s, masses kg, number densities m^-3. Return 0 or invalid=1.
   LRS q evolves by the same STF matrix. No tensor evolution/ODE solver. */
int he35_pair(double ma,double mb,double na,double nb,double kappa,
              double thermal[4],double stf[4],double rates[2]);
#endif
