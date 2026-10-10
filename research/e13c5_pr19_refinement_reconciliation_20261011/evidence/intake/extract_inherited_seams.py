#!/usr/bin/env python3
"""Inventory existing capture rows only. No scientific solver imports or execution."""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json

ROOT = Path("/workspace/scratch/7fd51143e473")
BASE = ROOT / "BASS_HE_E13C4_LOCAL_REMAINDER_ENCLOSURE_20261010_v1"
UPSTREAM = BASE / "inputs/e13c3/inputs/e13c2/inputs/upstream_e13c1"
OUT = ROOT / "e13c5_intake_work/INPUT_SEAM_INVENTORY.json"

def identity(path):
    raw = path.read_bytes()
    return {"path": str(path), "relative_to_e13c4": str(path.relative_to(BASE)),
            "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def table(path):
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        rows = []
        for row in reader:
            rows.append({"csv_line_number": reader.line_num, "row": dict(row)})
        fields = reader.fieldnames
    return rows, fields

def key(row):
    return [row["mode"], int(row["step"]), int(row["node"]), int(row["segment"])]

def same_float(x, y):
    return float(x).hex() == float(y).hex()

sources = [identity(BASE / "inputs/SIX_CONTROLS.json")]
controls = json.loads((BASE / "inputs/SIX_CONTROLS.json").read_text())["controls"]
requested = [(c["key"][0], c["key"][2]) for c in controls]
all_modes = {}
stages = {}
anchored_inventory = []
for mode in ("OFF", "GM", "KF"):
    capture = UPSTREAM / "evidence/capture" / mode
    for filename in ("SEGMENTS.csv", "NODES.csv", "AGGREGATE.csv"):
        path = capture / filename
        rows, fields = table(path)
        sources.append({**identity(path), "rows": len(rows), "columns": fields})
        if filename == "SEGMENTS.csv":
            bynode = defaultdict(list)
            for rec in rows:
                bynode[int(rec["row"]["node"])].append(rec)
                if float(rec["row"]["anchored"]) != 0.0:
                    r = rec["row"]
                    anchored_inventory.append({
                        "id": key(r), "csv_line_number": rec["csv_line_number"],
                        "a": r["a"], "b": r["b"], "e0": r["e0"], "h": r["h"],
                        "source_on": r["source_on"], "anchored": r["anchored"],
                        "active_captured_species": [s for s in ("HI", "HeI", "HeII")
                                                    if float(r["lambda_" + s]) > 0.0]
                    })
            for rr in bynode.values():
                rr.sort(key=lambda x: (int(x["row"]["step"]), int(x["row"]["segment"])))
            all_modes[mode] = bynode
    stage_path = UPSTREAM / "inputs" / (mode + "_STAGES.csv")
    stage_rows, stage_fields = table(stage_path)
    stages[mode] = {int(x["row"]["step"]): x for x in stage_rows}
    sources.append({**identity(stage_path), "rows": len(stage_rows), "columns": stage_fields})

chains = []
# Six existing selected node chains, plus a clearly marked optional HeII seam pointer.
for mode, node in requested + [("OFF", 1620)]:
    rr = all_modes[mode][node]
    ss = []
    for left_rec, right_rec in zip(rr, rr[1:]):
        left, right = left_rec["row"], right_rec["row"]
        active_left = [s for s in ("HI", "HeI", "HeII") if float(left["lambda_" + s]) > 0.0]
        active_right = [s for s in ("HI", "HeI", "HeII") if float(right["lambda_" + s]) > 0.0]
        ss.append({
            "left_id": key(left), "right_id": key(right),
            "left_csv_line": left_rec["csv_line_number"], "right_csv_line": right_rec["csv_line_number"],
            "same_s_coordinate_binary64": same_float(left["b"], right["a"]),
            "same_captured_photon_binary64": same_float(left["n"], right["f0"]),
            "same_eta_binary64": same_float(left["eta"], right["eta"]),
            "same_weight_binary64": same_float(left["weight"], right["weight"]),
            "source_on_changes": float(left["source_on"]) != float(right["source_on"]),
            "active_captured_species_left": active_left,
            "active_captured_species_right": active_right,
            "active_captured_species_change": active_left != active_right,
            "anchor_flag_left": left["anchored"], "anchor_flag_right": right["anchored"],
            "energy_seam_inputs_unmodified": {
                "left_e0_csv": left["e0"], "left_h_csv": left["h"],
                "right_e0_csv": right["e0"],
                "required_formula": "DeltaE = exact_lift(right_e0) - exact_lift(left_e0) * exp(-exact_lift(left_h))",
                "DeltaE_evaluated_here": False
            }
        })
    chains.append({
        "mode": mode, "node": node,
        "is_existing_e13c4_selected_node": (mode, node) in requested,
        "classification": "existing_selected_node_adjacent_capture" if (mode,node) in requested else "optional_HeII_event_pointer_not_a_selected_E13C4_control",
        "source": str((UPSTREAM / "evidence/capture" / mode / "SEGMENTS.csv").relative_to(BASE)),
        "segments": [{**rec, "stage_source": str((UPSTREAM/"inputs"/(mode+"_STAGES.csv")).relative_to(BASE)),
                      "stage": stages[mode][int(rec["row"]["step"])]} for rec in rr],
        "seams": ss
    })

result = {
    "schema": "bass-he-e13c5-inherited-seam-intake-v1",
    "role": "source inventory helper; no scientific final decision",
    "source_policy": "Read preserved CSV strings; only binary64 equality and nonzero flag checks. No solver imports, old reruns, coefficient evaluation, exponential evaluation, or physical claim.",
    "claim_ceiling": "Existing adjacent inputs are present and metadata-identifiable. This does not certify propagation, anchor bounds, native representation, or full path.",
    "sources": sources,
    "chains": chains,
    "all_captured_anchored_rows": anchored_inventory,
    "important_observations": [
        "OFF node0 source-on to source-off seam at step2 segment0->1 has both anchored flags zero; anchored alone is not a complete event selector.",
        "OFF node700 step2 segment0->1 is HeI opacity-on to opacity-off with source remaining on; both segments anchored1.",
        "OFF node1620 offers the analogous HeII event as an optional new small-control pointer.",
        "All selected node chains start with captured f0 zero in step1; carry-forward correction must not be reset at later captured f0.",
        "CSV energy and moment units must follow inherited E13C4 code/documentation; no unit conversion was performed in this inventory."
    ]
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
seams = [s for c in chains for s in c["seams"]]
print(json.dumps({
    "output": str(OUT), "bytes": OUT.stat().st_size,
    "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
    "source_files": len(sources), "chains": len(chains),
    "existing_selected_node_chains": sum(c["is_existing_e13c4_selected_node"] for c in chains),
    "seams": len(seams),
    "all_seams_s_contiguous_binary64": all(s["same_s_coordinate_binary64"] for s in seams),
    "all_seams_captured_photon_contiguous_binary64": all(s["same_captured_photon_binary64"] for s in seams),
    "all_seams_eta_and_weight_identical_binary64": all(s["same_eta_binary64"] and s["same_weight_binary64"] for s in seams),
    "scientific_solver_runs": 0
}, indent=2))

