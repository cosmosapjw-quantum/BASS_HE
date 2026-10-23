# HE37-H1DG: H1 differential ionization gain

**workflow1.0.0 / approval0.2**. Continues completed HE36 at `6403055c3d574ec0bd1ece80147f9711315902e7`.

This unit adopts one explicitly defined primary-source ionization approximation, derives its inclusive gain and net pressure source, and implements the matching number/energy/STF kernel in the sandbox. See CONTRACT.json for the original goal, present scope and remaining dependencies. DAG.json tracks R1–R10 → C1–C10 with per-stage archive and Git acknowledgements. Completed unchanged HE32–HE36 calculations are reused.

The selected source is the Le–Cambier semiclassical energy-sharing model (Eq85) with their isotropic outgoing directions (§III.E), subject to exact R2 source admission. The empirical calibration of H1 angular distributions remains a separate dependency.
