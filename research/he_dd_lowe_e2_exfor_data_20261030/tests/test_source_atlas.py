import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from build_source_atlas import EXPECTED,SELECT,M,m,Q,THRESHOLD,load_exact,parse_sources,make_dataset,run

class SourcePhysics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw,cls.manifest=load_exact(ROOT/'sources')
        cls.parsed=parse_sources(cls.raw)
        cls.dataset=make_dataset(cls.parsed,cls.manifest)

    def test_01_all_four_exact_sources(self):
        self.assertEqual(set(self.raw),set(EXPECTED))
        self.assertEqual(len(self.raw),4)
    def test_02_git_blob_matches_original(self):
        for k,spec in EXPECTED.items():
            b=(ROOT/'sources'/f'{k}.x4').read_bytes()
            sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            self.assertEqual(sha,spec['blob'])
    def test_03_sha256_and_bytes(self):
        for k,spec in EXPECTED.items():
            b=(ROOT/'sources'/f'{k}.x4').read_bytes()
            self.assertEqual((len(b),hashlib.sha256(b).hexdigest()),(spec['bytes'],spec['sha256']))
    def test_04_source_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td)
            for k in EXPECTED:shutil.copy2(ROOT/'sources'/f'{k}.x4',d/f'{k}.x4')
            p=d/'M0011.x4';p.write_bytes(p.read_bytes().replace(b'0.87',b'0.89',1))
            with self.assertRaisesRegex(ValueError,'drift'):load_exact(d)
    def test_05_subentry_grails(self):
        self.assertEqual(set(self.parsed),set(SELECT))
    def test_06_row_counts(self):
        n={k:len(v['rows']) for k,v in self.parsed.items()}
        self.assertEqual(n,{'M0011002':14,'M0011003':7,'M0826002':4,'M0826003':9,
                             'M0034005':14,'M0034006':9,'M0475002':12,'M0475003':6})
        self.assertEqual(sum(n.values()),75)
    def test_07_no_wrong_channel(self):
        self.assertNotIn('M0034002',self.parsed)
        self.assertNotIn('M0034003',self.parsed)
        self.assertNotIn('M0034004',self.parsed)
    def test_08_multipolarity_EP(self):
        for k in ['M0011003','M0034006']:
            self.assertEqual(self.parsed[k]['common']['POLAR'],2)
            self.assertIn(',EP,SIG',self.parsed[k]['reaction'])
    def test_09_beam_polarization_not_EP(self):
        self.assertEqual(self.dataset['data_status']['E2_EP'], 'electric_quadrupole_multipole_POLAR_2_NOT_PHOTON_BEAM_POLARIZATION')
    def test_10_Author_first_M0011_total(self):
        self.assertEqual((self.parsed['M0011002']['rows'][0]['EN'],self.parsed['M0011002']['rows'][0]['DATA']), (26,F('0.87')))
        self.assertEqual(self.parsed['M0011002']['status'],'AUTHOR_TABLE')
    def test_11_first_ep_is_E2(self):
        self.assertEqual(self.parsed['M0011003']['rows'][0]['DATA'],F('0.83'))
        self.assertEqual(self.parsed['M0011003']['rows'][0]['ERR-S'],F('0.40'))
    def test_12_ratio_at_26_exact(self):
        q=self.dataset['derived_nominal_multipole']['M0011_AUTHOR_TOTAL_E2_SAME_ENERGY'][0]
        self.assertEqual(F(q['E2_fraction_nominal']),F(83,87))
    def test_13_ratio_at_32_exact(self):
        q={F(x['E_MeV']):x for x in self.dataset['derived_nominal_multipole']['M0011_AUTHOR_TOTAL_E2_SAME_ENERGY']}
        self.assertEqual(F(q[F(32)]['E2_fraction_nominal']),F(127,511))
        self.assertEqual(F(q[F(32)]['nonE2_remainder_nominal_microbarn']),F('3.84'))
    def test_14_ratios_physical_nominal(self):
        qs=self.dataset['derived_nominal_multipole']['M0011_AUTHOR_TOTAL_E2_SAME_ENERGY']
        self.assertEqual(len(qs),7)
        self.assertTrue(all(0<=F(x['E2_fraction_nominal'])<=1 for x in qs))
    def test_15_E2_fraction_no_joint_CI(self):
        for z in self.dataset['derived_nominal_multipole']['M0011_AUTHOR_TOTAL_E2_SAME_ENERGY']:
            self.assertTrue(z['E2_share_joint_uncertainty'].startswith('UNKNOWN_COVARIANCE'))
    def test_16_m0034_digitized_not_another_independent(self):
        self.assertEqual(self.parsed['M0034005']['status'],'FIGURE_DIGITIZED')
        self.assertIn('NOT_INDEPENDENT',self.dataset['data_status']['M0034'])
    def test_17_first_source_compat(self):
        d=self.dataset['derived_nominal_multipole']['M0011_M0034_NEAR_ENERGY_DIAGNOSTIC']
        self.assertEqual(len(d),14)
        self.assertEqual(F(d[0]['M0011_E_MeV']),26)
        self.assertEqual(F(d[0]['M0034_E_MeV']),F('25.9'))
    def test_18_M0034_E2_source_difference(self):
        a={z['EN']:z['DATA'] for z in self.parsed['M0011003']['rows']}
        b={z['EN']:z['DATA'] for z in self.parsed['M0034006']['rows']}
        self.assertEqual(a[F(32)],F('1.27'))
        self.assertEqual(b[F(32)],F('2.72'))
    def test_19_M0826_window_true(self):
        z=self.parsed['M0826002']['rows']
        self.assertEqual([(x['EN-MIN'],x['EN-MAX']) for x in z],[(30,40),(40,50),(50,60),(60,75)])
    def test_20_angle_window_no_midpoint_as_measured(self):
        self.assertEqual(self.parsed['M0826003']['common'],{'EN-MIN':F(30),'EN-MAX':F(50)})
        xs=self.parsed['M0826003']['rows']
        self.assertEqual((xs[0]['ANG-CM-MIN'],xs[0]['ANG-CM-MAX']),(0,20))
        self.assertEqual((xs[-1]['ANG-CM-MIN'],xs[-1]['ANG-CM-MAX']),(160,180))
    def test_21_M0826_sys_distinct(self):
        self.assertIn('ERR-SYS,,5.',self.raw['M0826'])
        self.assertIn('not higher than 5',self.raw['M0826'])
    def test_22_binned_physical_K_support(self):
        z=self.dataset['dataset']['M0826002']['observations'][0]
        self.assertEqual(list(map(F,z['E_minus_Q_support_MeV'])),[F(30)-Q,F(40)-Q])
        self.assertEqual(list(map(F,z['sigma_times_pairK_conditional_support_source_unit_MeV'])),
                         [F('2.94')*(F(30)-Q),F('2.94')*(F(40)-Q)])
    def test_23_E2_at_26_weight_exact(self):
        z=self.dataset['dataset']['M0011003']['observations'][0]
        self.assertEqual(F(z['sigma_times_pairK_source_unit_MeV']),F('0.83')*(F(26)-Q))
    def test_24_M0011_SIG_at_26_weight_exact(self):
        z=self.dataset['dataset']['M0011002']['observations'][0]
        self.assertEqual(F(z['sigma_times_pairK_source_unit_MeV']),F('0.87')*(F(26)-Q))
    def test_25_recoil_threshold_exact(self):
        self.assertEqual(Q,F('23.84647820'))
        self.assertEqual(THRESHOLD,Q+Q*Q/(2*M))
        self.assertGreater(26,THRESHOLD)
    def test_26_M0475_SIG_no_330(self):
        self.assertNotIn(F(330),{z['EN'] for z in self.parsed['M0475003']['rows']})
    def test_27_units_distinct(self):
        self.assertEqual(self.parsed['M0475003']['units'],['MEV','NB','NB'])
        self.assertEqual(self.parsed['M0011002']['units'],['MEV','MICRO-B','MICRO-B'])
    def test_28_physics_HOLD(self):
        d=self.dataset['data_status']
        self.assertIsNone(d['kappa']);self.assertIsNone(d['R_event']);self.assertIsNone(d['heat_rate'])
        self.assertFalse(d['physical_activation']);self.assertFalse(d['L4']);self.assertEqual(d['production'],'HOLD')
    def test_29_all_positive_and_above_threshold(self):
        for blk in self.parsed.values():
            for r in blk['rows']:
                datum=r.get('DATA',r.get('DATA-CM'))
                self.assertGreaterEqual(datum,0)
                self.assertGreaterEqual(r['ERR-S'],0)
                if 'EN' in r:self.assertGreaterEqual(r['EN'],THRESHOLD)
    def test_30_total_observations_57_new(self):
        self.assertEqual(sum(len(x['rows']) for k,x in self.parsed.items() if not k.startswith('M0475')),57)
    def test_31_measured_vs_model_label(self):
        self.assertEqual(self.dataset['data_status']['M0011'],'AUTHOR_TABLE')
        self.assertEqual(self.dataset['data_status']['M0826'],'ENERGY_BIN_AND_ANGLE_BIN')
    def test_32_file_output_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            z=run(ROOT/'sources',Path(td));q=json.loads((Path(td)/'EXFOR_MULTI_SOURCE_ATLAS.json').read_text())
            self.assertEqual(z['row_totals'],q['row_totals'])
            self.assertTrue((Path(td)/'M0011_E2_SAME_ENERGY.csv').exists())
    def test_33_wrong_subentry_EP_rejected(self):
        bad=self.raw.copy();bad['M0011']=bad['M0011'].replace('POLAR\nNO-DIM\n 2.','POLAR\nNO-DIM\n 1.')
        with self.assertRaisesRegex(ValueError,'multipolarity'):parse_sources(bad)
    def test_34_invalid_unit_rejected(self):
        bad=self.raw.copy();bad['M0475']=bad['M0475'].replace('NB/SR','MB/SR',1)
        with self.assertRaisesRegex(ValueError,'header/units'):parse_sources(bad)
    def test_35_original_CRC_gate(self):
        self.assertEqual(self.manifest['M0034']['sha256'],'d1dbfa9e8899d91fa7c3993be6e22fd9d2aad0438084f09faf2906922eb3bd93')

if __name__=='__main__':unittest.main(verbosity=2)
