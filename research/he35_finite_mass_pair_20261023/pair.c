#include <math.h>
#include "pair.h"
int he35_pair(double ma,double mb,double na,double nb,double k,
              double t[4],double s[4],double r[2]) {
 double scale,a,b,x,y,f,d;
 if(!t||!s||!r||!isfinite(ma)||!isfinite(mb)||!isfinite(na)||!isfinite(nb)||!isfinite(k)||ma<=0||mb<=0||na<=0||nb<=0||k<0) return 1;
 if(k==0){for(int i=0;i<4;i++){t[i]=0;s[i]=0;}r[0]=0;r[1]=0;return 0;}
 scale=fmax(ma,mb);a=(ma/scale)/(ma/scale+mb/scale);b=(mb/scale)/(ma/scale+mb/scale);
 t[0]=-2*a*b*k*nb;t[1]=2*a*b*k*na;t[2]=-t[0];t[3]=-t[1];
 x=nb*b*(2*a+b);y=na*a*(2*b+a);
 s[0]=-k*x;s[1]=k*na*a*b;s[2]=k*nb*a*b;s[3]=-k*y;
 f=.5*(x+y+hypot(x-y,2*a*b*sqrt(na)*sqrt(nb)));d=2*na*nb*a*b;
 r[0]=k*(f ? d/f : 0);r[1]=k*f;
 for(int i=0;i<4;i++) if(!isfinite(t[i])||!isfinite(s[i]))return 1;
 return (!isfinite(r[0])||!isfinite(r[1]));
}
