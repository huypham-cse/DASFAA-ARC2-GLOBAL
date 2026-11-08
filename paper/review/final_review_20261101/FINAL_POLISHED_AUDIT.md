# Final polished manuscript claim audit

**Verdict: PASS within the scope below; same-family, provisional.**

Auditor: fresh gpt-6.1-sol / high. Date: 2026-11-01T14:21:32.805428+00:00. No prior reviewer verdict or executor interpretation was used as scientific evidence.

Current artifact: `paper/ARC2_Global_DASFAA2027_final.pdf`, 15 pages. SHA256: `dead152e05d6d76e8a92d05fe524fe4fdef28b170191fbae8869b3e01d3c1d9f`. The previous `reviewed.pdf` (`dca88a0ed884dc1ae062d78c88cc186e93b7f2a6ae541071cb134f641f5f9d9b`) is the preserved pre-correction snapshot.

One wording issue was found during this audit and visibly resolved by the author. No unresolved quantitative or comparative mismatch remains in the audited final artifact. This does not certify public artifact access, independent replication, universal novelty, or unconditional submission readiness.

## Scope and verification

Read `main.tex`, all eight `sections/*.tex`, all five `generated/*.tex`, `figures/mechanism.tex`, the empirical figures, and the 15-page PDF. Evidence consists of the specified scored arrays and machine-generated scoring JSON, executed source, locks/protocols, raw B2 seals/first-opening/encoding metadata, and primary literature. The existing operational `AGENTS.md` was not used as scientific evidence. Prior reviews, research narratives, generated claim/verification reports, qrel contents, and manuscript opinions were excluded as evidence.

No training, encoding, retrieval, ranking replay, qrel opening or rescoring was performed. I recomputed 400 condition metric means from scored arrays (320 development and 80 TREC values): maximum errors were 9.44e-16 and 5.55e-16. I compared saved B1c/B1M/B1P intervals and inspected their executed constructions. I did **not** rerun a full 20,000-draw metric bootstrap. I recomputed 340 TREC interval endpoints from the already saved `(20000,140)` bootstrap matrix: maximum error 0. I regenerated only the B1c/B2 RNG index streams and matched every saved digest.

All 80 development/TREC quality-plot CSV rows, including the eight native points, and all 15 ablation plot values agree with raw scoring output. An independent formatter checked 22 generated table rows / 111 numeric cells. Remaining ablation and family-count rows were checked directly. PDF text was extracted for every page; method equations and the empirical tables/figures were visually inspected. After the wording correction, the author finalized standard float settings (`topfraction=0.9`, `textfraction=0.1`). I re-read `main.tex`, extracted all 15 final PDF pages, confirmed the decimal-number multiset was unchanged, and re-rendered and inspected final pages 9?14. The empirical figures now appear on pages 10?12 and the all-paid table remains within Results. The corrected Full-X clause is on page 14.

## Resolved finding F01: Full-X comparison scope

Original sentence: ?every partial development ARC2 endpoint is below it.? All **24 five-seed condition means** are below native Full-X, but this is false for two individual seed endpoints:

| Development endpoint | ARC2 nDCG | Native Full-X nDCG | ARC2 minus Full-X |
|---|---:|---:|---:|
| NanoNQ / MiniLM / 75% / seed 17 | 0.6170579776857434 | 0.5930818641709094 | +0.023976113514834085 |
| NanoNQ / MiniLM / 75% / seed 53 | 0.5960056714437786 | 0.5930818641709094 | +0.0029238072728692277 |

The author changed the clause to ?every partial development five-seed ARC2 condition mean is below it.? I re-read `sections/discussion.tex` and verified that exact meaning in the rebuilt final PDF on page 14. The correction is supported; the initial finding and counterexamples remain in the JSON ledger.

## Exact development evidence

| Method | Macro nDCG@10 | Macro Recall@100 | ARC2 minus method: nDCG | Saved family interval |
|---|---:|---:|---:|---|
| arc2_global_tangent2_r1 | 0.5274775273004960 | 0.8658612474562474 | N/A | N/A |
| procrustes_global | 0.5031524182600609 | 0.8660998378473379 | 0.0243251090404352 | [0.018132175212397208, 0.030791640313948616] |
| la2m20_integration_script_adaptation | 0.4234225735192927 | 0.7758335509398009 | 0.1040549537812033 | [0.08607033208524335, 0.1229148044499058] |
| simplelinear_official_final50_mlp5 | 0.3553776623832738 | 0.6129790412827912 | 0.1720998649172223 | [0.1498621517850371, 0.19470300383538613] |
| ridge_affine_l10_bias_regularized | 0.4318244780276741 | 0.7441268305305805 | 0.0956530492728220 | [0.07540472081021199, 0.11642668663044543] |
| embedding_converter_paper_spec | 0.3663151931091557 | 0.7641036175861177 | 0.1611623341913405 | [0.14268641175964025, 0.17991558284155384] |

All five development family intervals are positive. Procrustes point gains occur in 23/24 conditions; each other baseline has 24/24 positive point differences. Pair-wise Procrustes macro differences are `0.025732936236754725` (MiniLM) and `0.022917281844115747` (E5). The sole negative Procrustes condition is FiQA/E5/75%, `-0.003583` at the paper precision. Recall versus Procrustes is unresolved: `[-0.004943626172438673, 0.0043358499949124945]`. All corresponding printed values round correctly.

## Exact ablation evidence

| Contrast | Exact macro nDCG delta | Saved 99% interval |
|---|---:|---|
| arc2_global_tangent2_r1 minus procrustes_global | 0.024325109040435233 | [0.01801533254696277, 0.03102132243820168] |
| arc2_global_tangent2_r1 minus tangent1_l10 | 0.006923862939737235 | [0.003809388309482942, 0.009959126205904258] |
| arc2_global_tangent2_r1 minus ridge_affine_l10_bias_regularized | 0.09565304927282199 | [0.07535298921225946, 0.11663127039230592] |
| tangent2_l1 minus arc2_global_tangent2_r1 | 0.0031974956912717346 | [-0.0018903844098364442, 0.00830403326634241] |
| tangent2_l100 minus arc2_global_tangent2_r1 | -0.00925533869678723 | [-0.01321398029023485, -0.005510245768211927] |

These are development estimates from the separate five-contrast mechanism family. The two-step/one-step value and interval match the paper. The ridge contrast combines initialization/prior and targeting; the paper now describes that scope correctly. The separate B1c and B1M zero-step/ridge interval endpoints legitimately differ because their bootstrap streams and inferential families differ.

## Prospective and all-paid evidence

TREC-COVID has 11 positive / 19 unresolved / 0 negative family intervals: Converter 5/6, ridge 4/6, SimpleLinear 2/6. All Procrustes and LA2M family intervals are unresolved; Procrustes point means exceed ARC2 in all six cells. These qualifications appear in the manuscript. E5 ARC2-minus-Converter exact deltas at 25/50/75% are `0.25723359077319435`, `0.23138457517015265`, and `0.1999540966512042`. The 25% family interval is `[0.17573076152800798, 0.33756850203860655]`. The abstract range and six-decimal prose round correctly.

MiniLM/75% ARC2 and native Full-Y round to 0.5195 and 0.5203; the paper explicitly declines an equivalence conclusion. The complete means and all 30 contrasts, including the exact unrounded native values, are recorded in JSON claim C11/C12.

All-paid MiniLM ARC2 nDCG is `0.36714602143626496`, versus fixed `0.3075048582716371`: all-paid beats Procrustes, LA2M, SimpleLinear and Converter under the 32-contrast family; ridge is unresolved. All-paid E5 is `0.29186698206096195`, versus fixed `0.3116352075358866`: it trails Procrustes/LA2M, beats SimpleLinear/ridge, and is unresolved against Converter. The E5 within-method interval is `[-0.056329874306672884, 0.016636927373489714]`. Fixed MiniLM ARC2 is below all five all-paid baseline intervals. The summed-objective lambda10 qualification is accurate.

For all-paid E5, proxy-only to mixed nDCG is `0.31490775036459107 -> 0.29186698206096207`, Recall is `0.6541642457542457 -> 0.5594899234099234`, and paid top-10 share is `0.49164 -> 0.06472000000000001`. MiniLM nDCG is `0.3509507352060274 -> 0.36714602143626507`. These are descriptive replacement diagnostics, as the paper presents them.

## Method, statistical and literature checks

The corrected normalization `N(z)=z/||z||` agrees with the actual source. The target is `r[y-(uy^T)u] = -r^2 grad(1-y N(z)^T)`. The ridge penalty is on the **correction**, including its intercept. Substitution `C=B_t+Delta` gives the stated prior centered on the **current** map. The source recomputes targets for exactly two updates at lambda10; float64 accumulation, float32 final storage, and reusable Cholesky agree. The text correctly avoids claiming every finite fitted update decreases cosine loss. Global positive scale equivariance is correctly restricted to exact arithmetic with nonzero predictions.

Shared-bootstrap-indices wording matches the executed construction for B1c, B1M, B1P recovery and B2. Queries are resampled within collections after five-seed averaging; the same collection indices are reused across the methods, budgets and migrations of each analysis. Family sizes 5/5/32/30 and descriptive Recall coverage are accurate. B1c/B1M/B1P scorer file hashes match saved execution identities; B2 source canonical-LF hashes match its immutable lock.

Coefficient accounting is exact: `385*768=295680`, `1182720` float32 bytes, `1.1279296875 MiB`; Converter has `33927168` parameters, giving ratio `114.74285714285715`. Thus 1.13 MiB and 114.7x are correct structural storage comparisons. The manuscript separates these from physical encoding time, fitting workspace, index resources and serving costs.

The HMoE paragraph is supported by the [primary PMLR page](https://proceedings.mlr.press/v306/yang26e.html) and cached primary paper text, particularly its localized hierarchical experts and Section 4 target-PC1/PC2 residual channels for mixing/chaining. The paper correctly positions HMoE as related work and does not claim it was in the five-baseline evaluated panel. Nearby literature descriptions were spot-traced to primary cached text; this audit is not a comprehensive novelty search or bibliographic certification.

## Artifact availability and prospective seal

The separate local R3 archive exists: `D:\DASFAA-2027-paper-release-20261101-r3-paper-story.zip`, 372,032,202 bytes, SHA256 `46e511a935d2068e86c4c19532fe4ad7a0b5e00a36018452f78705bd889b7a3e`. Its ZIP inventory contains code, baseline configuration, protocol and scored-source entries. I selectively inspected inventory availability; I did not revalidate its complete manifest or rerun it on a clean machine.

The current footnote accurately says the anonymous public link is pending. The paper does not provide an anonymous public evidence-download URL. Local packaging must not be described as already publicly available.

B2 raw receipts verify all 184 endpoint identities/order checks before first label opening. Verifier completion: `2026-10-31T20:11:42.810083+00:00`; first-opening receipt: `2026-10-31T20:12:17.410541+00:00`. Ranking/verification seal hashes and lock binding match. This audit checked those raw receipts without reopening labels or replaying retrieval.

## Claim-group ledger

| Group | Location | Status |
|---|---|---|
| C01 | abstract; introduction; experimental-setup | exact_match |
| C02 | method3.1; setup matched supervision | exact_match |
| C03 | method3.2 Eqs2-3 | exact_match |
| C04 | method3.3 Eqs4-8; algorithm; abstract | exact_match |
| C05 | method3.4-3.5; discussion; abstract | rounding_ok |
| C06 | setup comparison methods; related work | exact_match |
| C07 | setup retrieval and inference | exact_match |
| C08 | abstract; introduction; results5.1; generated/dev_macro.tex | rounding_ok |
| C09 | results5.1 | rounding_ok |
| C10 | abstract; introduction; results5.2; generated/ablation.tex; Figure3 | rounding_ok |
| C11 | abstract; introduction; results5.3; generated/trec_means.tex,trec_family.tex; Figure4 | rounding_ok |
| C12 | abstract; results5.3; discussion | rounding_ok |
| C13 | results5.4; generated/allpaid.tex | rounding_ok |
| C14 | results5.4 mixed-gallery paragraph | rounding_ok |
| C15 | discussion paragraph2; finalPDFp13 | exact_match |
| C16 | related-work HMoE paragraph and nearest-method positioning | exact_match |
| C17 | Figures1-4; all generated tex | rounding_ok |
| C18 | setup availability footnote; prospective scope | exact_match |

There are 18 claim groups, zero unresolved mismatches, and one resolved wording finding. Exact values for all reported means, all 30 prospective contrasts, all 32 all-paid contrasts and gallery controls are embedded in the JSON. The adjacent `audit_calculations.json` preserves independent calculations and check detail.

## Unverified / readiness ledger

- Anonymous public access remains pending, truthfully disclosed in the manuscript.
- Full encoding, training, retrieval, label scoring and full bootstrap regeneration were not repeated. Saved-scored-output fidelity and mathematical/code agreement are the audited scope.
- This fresh OpenAI-family audit is same-family and provisional. It does not establish independent replication, comprehensive novelty, or an unconditional submission-ready verdict.

## Final input hashes

The authoritative `audited_input_hashes` map is in `FINAL_POLISHED_AUDIT.json`: in-paper paths are relative to `paper/`; outside scientific inputs use absolute paths. Hashes were captured after verifying the author?s correction and rebuilt final PDF. The old PDF hash is retained explicitly so the current PASS cannot be confused with the previous artifact.
