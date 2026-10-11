#!/usr/bin/env python3
"""Read-only numerical summaries and publication plots; no physics execution."""
from pathlib import Path
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def dec(x):
    with localcontext() as ctx:
        ctx.prec = 50
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def box(v):
    return F(v['lo']), F(v['hi'])


def final_boxes(t):
    out = {k: box(v['interval']) for k, v in t['cumulative_moment_corrections'].items()}
    out['P1'] = box(t['final_photon']['true_minus_captured_interval'])
    out['P1_energy_eV'] = box(t['final_energy_stock_eV']['true_minus_captured_interval'])
    return out


def main():
    names = ['N32_P60', 'N128_P60', 'N512_P60', 'N32_P80']
    runs = {name: json.loads((ROOT / 'evidence' / (name + '.json')).read_text()) for name in names}
    primary = runs['N512_P60']
    checks, diagnostics, summaries = [], [], []
    for name, run in runs.items():
        wrapper = json.loads((ROOT / 'evidence' / ('run_' + name) / 'RUN.json').read_text())
        checks.append({'id': name + '_actual_exit_and_source', 'pass': wrapper['actual_exit'] == 0 and run['source_unchanged_during_run']})
    for i, t in enumerate(primary['tracks']):
        comparisons = []
        for coarse, fine in [('N32_P60', 'N128_P60'), ('N128_P60', 'N512_P60'), ('N32_P60', 'N32_P80')]:
            a, b = final_boxes(runs[coarse]['tracks'][i]), final_boxes(runs[fine]['tracks'][i])
            for k in a:
                overlap = max(a[k][0], b[k][0]) <= min(a[k][1], b[k][1])
                nested = a[k][0] <= b[k][0] <= b[k][1] <= a[k][1]
                checks.append({'id': f'compatible_{t["track"]["node"]}_{k}_{coarse}_{fine}', 'pass': overlap})
                comparisons.append({'coarse': coarse, 'fine': fine, 'observable': k, 'intervals_overlap': overlap, 'fine_subset_coarse': nested})
        heat = t['cumulative_moment_corrections']['H_total_eV']
        photon = t['final_photon']
        budget = {name: sum((F(r['remainder'][name]['H_total_eV']) for r in t['segments']), F(0))
                  for name in ('incoming_upper', 'nonlinear_upper')}
        budget['numerical_and_representation'] = sum((F(r['outputs']['H_total_eV']['numerical_and_representation_radius']) for r in t['segments']), F(0))
        budget['outward_accumulation_excess'] = F(heat['radius']) - sum(budget.values(), F(0))
        h0, h1 = runs['N32_P60']['tracks'][i]['cumulative_moment_corrections']['H_total_eV'], runs['N32_P80']['tracks'][i]['cumulative_moment_corrections']['H_total_eV']
        summary = {'track': t['track'], 'final_photon': photon, 'cumulative_heat_eV': heat,
                   'heat_radius_over_abs_correction_diagnostic': dec(F(heat['radius']) / abs(F(heat['candidate']))),
                   'photon_radius_over_abs_correction_diagnostic': dec(F(photon['radius']) / abs(F(photon['candidate']))),
                   'heat_budget_eV': {k: dec(v) for k, v in budget.items()},
                   'heat_budget_fraction_diagnostic': {k: dec(v / F(heat['radius'])) for k, v in budget.items()},
                   'N32_precision60_vs80_heat_center_abs_gap': dec(abs(F(h0['candidate']) - F(h1['candidate']))),
                   'N32_precision_center_gap_over_P60_radius': dec(abs(F(h0['candidate']) - F(h1['candidate'])) / F(h0['radius'])),
                   'heat_radius_N32_over_N512': dec(F(h0['radius']) / F(heat['radius'])),
                   'global_ledger_enclosures': t['global_ledger_enclosures'],
                   'seams': [{k: s[k] for k in ('left', 'right', 'DeltaE_eV', 'correction_anchor_relative_to_captured_photon_eV', 'true_anchor_eV')} for s in t['seams']]}
        summaries.append(summary)
        diagnostics.extend(comparisons)
    physical = {'schema': 'bass-he-e13c5-physical-result-v1', 'evidence_status': ['derived', 'numerically_checked', 'implementation_verified'],
                'owner_status': 'BOUNDED_EXECUTION_COMPLETE_INDEPENDENT_DECISION_SEPARATE',
                'scope': 'two OFF nodes0/700 three-segment tracks; exact real sum of captured persegment moments; fixed gas/masks/anchors',
                'reference_accuracy_assumed_for_bounds': False, 'tracks': summaries,
                'actual_runs': [{k: runs[name][k] for k in ('elapsed_seconds', 'peak_RSS_KiB', 'new_coefficient_evaluations', 'reused_local_enclosures', 'new_local_enclosures')} | {'name': name, 'actual_exit': 0} for name in names],
                'all_new_coefficient_evaluations': sum(r['new_coefficient_evaluations'] for r in runs.values()),
                'new_scientific_kernel_seconds': sum(r['elapsed_seconds'] for r in runs.values()),
                'actual_NCP_execution': 'NO_RETURN_FOUND_IN_SCOPED_SEARCH_E13C4; E13C5_PREPARED_NOT_RUN_ON_NCP',
                'physical': 'HOLD', 'production': 'HOLD', 'uniform_fullpath_certificate': False,
                'native_aggregate_reduction_certificate': False, 'actual_atomic_photon_heat_recoil': None}
    acceptance = {'schema': 'bass-he-e13c5-owner-saved-evidence-check-v1', 'role': 'OWNER_SELF_REVIEW',
                  'physics_reexecution': False, 'checks': checks, 'pass_count': sum(c['pass'] for c in checks),
                  'fail_count': sum(not c['pass'] for c in checks), 'refinement_and_precision_diagnostics': diagnostics,
                  'diagnostic_scope': 'interval overlap/nesting is consistency evidence; inclusion comes from analytic+arithmetic arguments, not refinement',
                  'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'input_sha256': {name: hashlib.sha256((ROOT / 'evidence' / (name + '.json')).read_bytes()).hexdigest() for name in names}}
    for name, obj in [('PHYSICAL_RESULT.json', physical), ('evidence/OWNER_SAVED_EVIDENCE_CHECK.json', acceptance)]:
        (ROOT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')
    make_figure(runs)
    print(json.dumps({'pass': acceptance['pass_count'], 'fail': acceptance['fail_count'], 'physics_reexecution': False,
                      'new_scientific_kernel_seconds': physical['new_scientific_kernel_seconds']}))
    return 0 if acceptance['fail_count'] == 0 else 1


def make_figure(runs):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.7), constrained_layout=True)
    colors = ['#3366A0', '#B56A28', '#6D4D8A']
    for idx, node in enumerate((0, 700)):
        scale = 1e-14 if node == 0 else 1e-12
        unit = r'$10^{-14}$' if node == 0 else r'$10^{-12}$'
        names = ['N32_P60', 'N128_P60', 'N512_P60']
        vals = [runs[n]['tracks'][idx]['cumulative_moment_corrections']['H_total_eV'] for n in names]
        ax = axes[0, idx]
        ax.errorbar([32, 128, 512], [float(v['candidate']) / scale for v in vals],
                    yerr=[float(v['radius']) / scale for v in vals], marker='o', color=colors[0],
                    capsize=5, linewidth=1.6)
        ax.set_xscale('log', base=4); ax.set_xticks([32, 128, 512], ['32', '128', '512'])
        ax.set_xlabel('Validated midpoint cells per segment')
        ax.set_ylabel('Cumulative heat correction / ' + unit + ' eV norm.')
        ax.set_title(f'OFF node {node} | three captured segments', loc='left', weight='bold')
        ax.grid(axis='y', alpha=.2)
        bottom = np.zeros(3)
        ax = axes[1, idx]
        for key, label, color in [('numerical', 'Integral / representation enclosure', colors[0]),
                                  ('incoming', 'Carried incoming uncertainty', colors[1]),
                                  ('nonlinear', 'First-variation remainder', colors[2])]:
            values = []
            for n in names:
                rows = runs[n]['tracks'][idx]['segments']
                if key == 'numerical':
                    v = sum(float(r['outputs']['H_total_eV']['numerical_and_representation_radius']) for r in rows)
                else:
                    v = sum(float(r['remainder'][key + '_upper']['H_total_eV']) for r in rows)
                total = float(runs[n]['tracks'][idx]['cumulative_moment_corrections']['H_total_eV']['radius'])
                values.append(v / total)
            ax.bar(range(3), values, bottom=bottom, color=color, width=.58, label=label)
            bottom += values
        ax.set_xticks(range(3), ['N32', 'N128', 'N512'])
        ax.set_ylim(0, 1.14); ax.set_yticks([0, .2, .4, .6, .8, 1]); ax.set_ylabel('Fraction of the absolute heat-error bound')
        ax.set_title('Error budget carried across both seams', loc='left')
        for j, v in enumerate(vals):
            ax.text(j, 1.035, f"{float(v['radius']):.3g} eV", ha='center', va='bottom', fontsize=9)
    handles, labels = axes[1, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='outside lower center', ncol=3, frameon=False, fontsize=9)
    fig.suptitle('BASS_HE E13C5 | certified bounds on two fixed-gas tracks', x=.015, ha='left', fontsize=16, weight='bold')
    (ROOT / 'figures').mkdir(exist_ok=True)
    fig.savefig(ROOT / 'figures/INCOMING_ANCHOR_ENCLOSURE.png', dpi=180, facecolor='white')
    fig.savefig(ROOT / 'figures/INCOMING_ANCHOR_ENCLOSURE.svg', facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    raise SystemExit(main())
