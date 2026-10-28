"""New full-law trace oracle via direct two-daughter high-precision integration."""
from pathlib import Path
import json,sys
from fractions import Fraction
import mpmath as mp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from energy_gain import SexticLaw,FULL_WITNESS
from nonthermal_d_birth import HE4_REST_MEV,D_REST_MEV,GAMMA_MEV,K0_MEV

law=SexticLaw(FULL_WITNESS)
def mpr(x):return mp.mpf(x.numerator)/x.denominator

def direct(dps):
 with mp.workdps(dps):
  a=mp.mpf('3727.3794118');m=mp.mpf('1875.61294500');e=mp.mpf(330)
  s=a*a+2*a*e;b=e*mp.sqrt(s/4-m*m)/mp.sqrt(s);e0=(a+e)/2
  z=mp.mpf(14297)/52500
  def fun(u):
   q=(1-u*u)*(mp.mpf(1411)/10000-u*u/4+mp.mpf(33)/25*u**4)/z
   ep=e0+b*u;em=e0-b*u
   return q*((ep*ep-m*m)/ep+(em*em-m*m)/em)
  out=mp.quad(fun,[-1,0,1])
  return mp.nstr(out,dps)

values={str(n):direct(n) for n in (50,80)}
with mp.workdps(85):
 v=mp.mpf(values['80']);delta=abs(v-mp.mpf(values['50']))
 oracle_uncertainty=delta+mp.mpf('1e-45')
 intervals=[]
 for n in range(7):
  t=law.trace_enclosure(n);lo=mpr(t['lower_MeV_per_event']);hi=mpr(t['upper_MeV_per_event'])
  inside=lo-oracle_uncertainty<=v<=hi+oracle_uncertainty
  if not inside:raise AssertionError('independent quadrature outside exact interval')
  intervals.append(dict(order=n,lower_exact=str(t['lower_MeV_per_event']),upper_exact=str(t['upper_MeV_per_event']),width_exact=str(t['width_MeV_per_event']),lower_decimal=mp.nstr(lo,45),upper_decimal=mp.nstr(hi,45),width_decimal=mp.nstr(hi-lo,12),quadrature_inside=bool(inside)))
 bins=law.bins(('-1','-4/5','-1/5','2/5','1'))
 wrong=sum(b['number']*(b['lo_x']+b['hi_x'])/2 for b in bins)
 result={'scope':'chosen normalized sextic law, conditional event; no rate or physical activation',
  'method':'mpmath adaptive quadrature of direct sum [(Eplus^2-M^2)/Eplus+(Eminus^2-M^2)/Eminus] times explicit normalized q; independent of moment series',
  'mpmath_version':mp.__version__,'reference_MeV_per_event':values,'precision_difference':mp.nstr(delta,15),
  'numerical_oracle_uncertainty':mp.nstr(oracle_uncertainty,15),'oracle_is_rigorous_interval':False,
  'intervals':intervals,'r':str(law.trace_enclosure(0)['r']),
  'm2':str(law.even_moment(1)),'bin_number_total':str(sum(b['number'] for b in bins)),
  'bin_first_x_total':str(sum(b['first_x'] for b in bins)),
  'midpoint_mutant_first_x':str(wrong),'midpoint_mutant_kinetic_error_MeV':mp.nstr(mp.sqrt(mpr(law.trace_enclosure(0)['r']))*mpr((HE4_REST_MEV+GAMMA_MEV)/2)*mpr(wrong),15),
  'bins':[{k:str(v) for k,v in b.items()} for b in bins],
  'new_physical_IVPs':0,'old_science_replays':0,'physical_activation':False,'L4':False}
(ROOT/'evidence/NUMERICAL_REFERENCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'trace_MeV_per_event':values['80'],'order4_width_MeV_per_event':intervals[4]['width_decimal'],'all7_enclosures_contain_reference':all(t['quadrature_inside'] for t in intervals),'precision_difference':result['precision_difference'],'midpoint_mutant_kinetic_error_MeV':result['midpoint_mutant_kinetic_error_MeV']}))
