"""Synthetic simultaneous-premise and finite-induction traps, no native math."""
from copy import deepcopy
from fractions import Fraction as F
import unittest
from be_replay import finite1519_join_interfaces as join


def fixture(n=15):
    source=dict(pl='1/2',pu='51/100',beta_lo='-1/2',beta='1/2',mean_lo='1/10',mean_hi='1/5')
    raw=dict(pl='1/2',pu='51/100',A='1',B='1',beta_lo='-1/2',beta_hi_signed='1/2',mean_hi='1/5')
    q=dict(A='1',Fplus='1/10',Fminus='1/5',Qbudget='1/2')
    r=dict(N=n,index=50,K='0',pl='1/2',pu='51/100',rho_hi='11/10',
        D='1',charge_b='9/10',charge_g='1',charge_h='1/2',d0='1/10',lambda_max='1/5',
        H_minus='1',H_plus='1',radius_minus='2',radius_plus='2',outer0='1',outer1='1',quadratics=[q])
    cfg=dict(n=n,index=50,K='0',p=['1/2','51/100'],rho_lower='1',rho_upper='11/10',D='1',d0='1/10',Lambda='1/5',
        Hminus='1',Hplus='1',radius_minus='2',radius_plus='2',outer0='1',outer1='1',
        binary_charge='9/10',gap_charge='1',noise_charge='1/2',acquired_lambda_upper='1/5',
        acquired_beta=['-1/2','1/2'],acquired_mean=['1/10','1/5'],quadratics=[deepcopy(q)],
        sign_premise=dict(conditional_means_zero=True,schema='ACTUAL_SIGN_CONDITIONED_MARGINAL_V1',
            resource_status='ASSUMED_ACQUIRED_FOR_CONDITIONAL_TEST',negative_endpoint_lower='1',positive_endpoint_lower='1'))
    return dict(source=source,result=dict(result=r,raw_row=raw)),cfg


class Interfaces(unittest.TestCase):
    def test_original_literal15_and16_19_source_conditions_retained(self):
        self.assertEqual(set(join.verify_reference_projection()),{'actual15.py','sequential.py'})
        for n in range(15,20):
            with self.subTest(n=n):join.interface(*fixture(n),'B0',50,n)

    def test_no_replacing_original_lambda_by_an_extra_cap(self):
        for n in(15,16,19):
            row,cfg=fixture(n);cfg['Lambda']=cfg['acquired_lambda_upper']='1/10'
            with self.subTest(n=n),self.assertRaises(ValueError):join.interface(row,cfg,'B0',50,n)

    def test_simultaneous_physical_charge_and_phase_rounding_traps(self):
        changes=[lambda c:c.update(gap_charge='999999/1000000'),
                 lambda c:c.update(noise_charge='499999/1000000'),
                 lambda c:c.update(acquired_beta=['-1/4','1/2']),
                 lambda c:c.update(acquired_mean=['1/10','19/100']),
                 lambda c:c.update(p=['1/2','101/200']),
                 lambda c:c.update(rho_lower='1000001/1000000'),
                 lambda c:c['sign_premise'].update(negative_endpoint_lower='1000001/1000000'),
                 lambda c:c['sign_premise'].update(conditional_means_zero=1),
                 lambda c:c['quadratics'][0].update(Qbudget='500001/1000000')]
        for n in(15,17):
            for i,change in enumerate(changes):
                row,cfg=fixture(n);change(cfg)
                with self.subTest(n=n,case=i),self.assertRaises(ValueError):join.interface(row,cfg,'B0',50,n)

    def test_all_count_roots_domain_and_literal_scope_preserved(self):
        for mutate in(lambda c:c.update(n=True),lambda c:c.update(index=True),
                      lambda c:c.update(Hminus='8'),lambda c:c.update(d0='1/2'),
                      lambda c:c.update(Lambda='20'),lambda c:c.update(K='1')):
            row,cfg=fixture();mutate(cfg)
            with self.assertRaises(ValueError):join.interface(row,cfg,'B0',50,15)
        for n,index in((True,50),(14,50),(20,50),(15,True),(15,100)):
            with self.subTest(n=n,index=index),self.assertRaises(ValueError):join.interface(*fixture(), 'B0',index,n)

    def test_resource_actual_index_cannot_be_borrowed_from_neighbor(self):
        row,cfg=fixture(18);row['result']['result']['N']=17
        with self.assertRaises(ValueError):join.interface(row,cfg,'B0',50,18)

    def test_no_skipped_predecessor_or_truthy_global_claim(self):
        local={n:True for n in range(15,20)}
        self.assertTrue(all(r['conditional_finite_result_established']for r in join.sequential(True,local)))
        self.assertFalse(any(r['conditional_finite_result_established']for r in join.sequential(False,local)))
        local[17]=False
        self.assertEqual([r['conditional_finite_result_established']for r in join.sequential(True,local)],
                         [True,True,False,False,False])
        for base,rows in((1,local),(True,{15:True,17:True,18:True,19:True}),(True,{**local,17:1})):
            with self.assertRaises(ValueError):join.sequential(base,rows)


if __name__=='__main__':unittest.main()
