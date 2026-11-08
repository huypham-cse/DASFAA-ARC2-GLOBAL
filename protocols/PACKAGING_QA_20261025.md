# Packaging and synthetic identity verification

Scope: extract the existing selected ARC2-Global computation into a standalone
package; copy only its FiQA rows and two external-baseline rows plus full-X/Y
references; reuse the existing paper's template/bibliography and section layout.
No benchmark inference, qrel reads, fresh metric scoring, GPU or independent
claim audit is authorized. The source repositories/archived draft stay intact.

Commit code/config/exporter/this record before synthetic execution. Use seeded
synthetic normalized float32 pairs (same and unequal dimensions), compare the
standalone implementation with the existing evaluated implementation in the
same process/runtime: base/one-step/final coefficients, proxy vectors, mixed
gallery, selected IDs. Require exact array equality; preserve failure receipts.
Exercise invalid budgets, missing anchors, changed anchor vectors and tiny
block handling. Copy hashes and imported per-query arithmetic must verify.

The archive is D:/DASFAA-2027-paper-before-arc2-global-20261025. Its earlier Git
history and draft remain there. The source run is the completed R10 development
run in D:/DASFAA-2027-MixIndex; its identity is retained in provenance, not
relabelled as a new experiment. A subset seal is an export receipt, not a new
pre-label scientific seal. Do not transfer old method-specific significance
intervals to the selected method.

After local packaging checks and paper build: STOP and report paths/verification
to the user. H100 preparation/execution/scoring and claim audits are future work.
