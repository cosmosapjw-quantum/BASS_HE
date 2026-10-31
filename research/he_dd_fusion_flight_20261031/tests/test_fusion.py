import math,unittest,sys,pathlib
from fastd_fusion import *
from fastd import plasma, terminal

class BoschHaleAndDeuteronTest(unittest.TestCase):
    def test_bh_benchmark_3kev(self):
        self.assertAlmostEqual(sigma_bh_mb(3,'dd_nhe3')/2.445e-4,1,places=3)
        self.assertAlmostEqual(sigma_bh_mb(3,'dd_pt')/2.513e-4,1,places=3)
    def test_bh_benchmark_10kev(self):
        self.assertAlmostEqual(sigma_bh_mb(10,'dd_nhe3')/0.2779,1,places=3)
        self.assertAlmostEqual(sigma_bh_mb(10,'dd_pt')/0.2812,1,places=3)
    def test_bh_benchmark_20kev(self):
        self.assertAlmostEqual(sigma_bh_mb(20,'dd_nhe3')/2.691,1,places=3)
    def test_low_out_of_range(self):
        with self.assertRaises(ValueError):sigma_bh_mb(.49,'dd_pt')
    def test_high_out_of_range(self):
        with self.assertRaises(ValueError):sigma_bh_mb(5001,'dd_pt')
    def test_nuclear_source_only_positive(self):
        for e in [1,10,30,100,1000,4000]:
            for c in COEFF: self.assertGreater(sigma_bh_mb(e,c),0)
    def test_invalid_channel(self):
        with self.assertRaises(ValueError):sigma_bh_mb(200,'dd_to_heat')
    def test_Q_values(self):
        self.assertAlmostEqual(Q_MEV['dd_nhe3'],3.26885719,places=6)
        self.assertAlmostEqual(Q_MEV['dd_pt'],4.03266400,places=6)
    def test_low_end_stopping(self):
        p=plasma(1e5)
        self.assertTrue(1e-3<=terminal(p)<=.01)
    def test_inflight_probability(self):
        r=integrate(1.,plasma(1e5),order=160)
        self.assertLess(r['P_any_BH_DD_fusion'],1e-7);self.assertGreater(r['P_any_BH_DD_fusion'],0)
        self.assertLess(abs(r['P_any_BH_DD_fusion']+r['P_no_BH_DD_fusion']-1),1e-12)
    def test_channels_probability(self):
        r=integrate(3.,plasma(1e5))
        self.assertAlmostEqual(r['P_nhe3']+r['P_pt'],r['P_any_BH_DD_fusion'],places=14)
    def test_DH_linear_optical_depth(self):
        p=plasma(1e5);r=integrate(1.,p,dh=D_H)
        s=integrate(1.,p,dh=D_H*2)
        self.assertAlmostEqual(s['tau_total_DD']/r['tau_total_DD'],2.,places=9)
    def test_joint_P_survival(self):
        r=integrate(8.,plasma(1e5))
        self.assertAlmostEqual(r['P_any_BH_DD_fusion'], -math.expm1(-r['tau_total_DD']),places=13)
    def test_k_monotonic(self):
        p=plasma(1e5)
        self.assertGreater(integrate(3.,p)['P_any_BH_DD_fusion'],integrate(.3,p)['P_any_BH_DD_fusion'])
    def test_reject_outside_high_fit(self):
        with self.assertRaises(ValueError):integrate(10.,plasma(1e5))
    def test_no_zero_yield(self):
        with self.assertRaises(ValueError):integrate(1.,plasma(1e5),dh=0)
    def test_energy_ledger_secondary_CM(self):
        r=integrate(1.,plasma(1e5))
        for channel in COEFF:
            sec=channel_secondary(r,channel)
            self.assertAlmostEqual(sec['mean_total_product_CM_K_MeV'],sec['mean_reaction_Ecm_MeV']+sec['Q_MeV'],places=12)
            self.assertEqual(sec['product_heat'],'NOT_COMPUTED')
    def test_quadrature_agrees(self):
        p=plasma(1e5);a=integrate(8.,p,160);b=integrate(8.,p,320)
        self.assertLess(abs(a['P_any_BH_DD_fusion']/b['P_any_BH_DD_fusion']-1),1e-3)
    def test_profile_source_domain(self):
        p=plasma(1e5);q=profile(1,p,21)
        self.assertEqual(len(q),21)
        self.assertGreaterEqual(q[-1]['Ecm_keV'],0.5-1e-10)
    def test_no_strong_heating_claim(self):
        r=integrate(1.,plasma(1e5))
        self.assertEqual(r['secondary_deposition'],'NOT_COMPUTED')
        self.assertLess(r['expected_binding_release_MeV'],1e-6)

if __name__=='__main__':unittest.main()
