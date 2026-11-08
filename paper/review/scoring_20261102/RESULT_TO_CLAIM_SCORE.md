# Fresh result-to-claim score: current bounded ARC2-Global paper

**Verdict: claim_supported = yes; confidence = high.** The current manuscript is supported within its stated conditions. I found no material unsupported empirical claim in its present wording. This is a same-family, provisional semantic review by **gpt-6.1-sol/high**, not an acceptance probability or holistic venue score.

Current PDF: `paper/ARC2_Global_DASFAA2027_final.pdf`, 16 pages, SHA256 `e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc`. I read its actual extracted text and inspected renders covering all pages, alongside all current section and generated-table TeX files. The ten supplied evidence-precheck matches establish value existence only; the judgments below use the raw records.

## Dimension scores

| Dimension | Score / 10 | Reason |
|---|---:|---|
| Empirical support | **8** | Strong direct support for the current bounded findings: complete development breadth, mechanism controls, recorded prospective matched-budget evidence and per-query consistency. It is below 9 because independent confirmation is one 50-query collection with two fixed migrations, and does not establish an nDCG win over the strongest geometric alternatives or a prospective second-step benefit. Those are limits on evidence breadth, not contradictions of the written claim. |
| Fairness / rigor | **8** | Shared anchor-inclusive exposure, the full five-baseline panel, native references, exact search, seed averaging before query resampling, explicit family correction and the recorded pre-label endpoint gate are substantial strengths. Baselines are openly declared adaptations, with paired-MAE Converter selection and fixed SimpleLinear training rather than equally tuned original-paper optima. DEV selection remains exposed; bootstrap coverage is approximate and conditional on fixed seeds/tasks. The audit does not independently reexecute remote provenance. |
| Practical value under the stated scenario | **7** | A useful compact candidate when destination queries are required and document replacement is staged: lower-exposure E5 points, no neural mapper training, all-paid MiniLM improvement and a small final map. Procrustes/LA2M remain competitive on the held collection and incumbent Full-X often has better quality if source queries are acceptable. Value is demonstrated in quality/exposure and storage, while deployment time, index resources, ANN and SLOs remain unmeasured. Those systems studies are optional extensions for the current claims. |
| Claim calibration | **9** | Current manuscript consistently separates DEV from held confirmation, matched-budget inference from post-hoc cross-budget point comparisons, auxiliary Recall from primary nDCG, geometric unresolved results from superiority, and structural storage from physical cost. Negative E5 all-paid and Full-X outcomes remain visible. It avoids universal-best, native-equivalence and physical-savings claims. Broad closing practical language is reasonably bounded by the explicit scenario and resource limitations. |

Anchors: 1-3 = little relevant evidence or serious contradiction; 4-6 = substantive but incomplete support; 7-8 = strong bounded support with meaningful breadth/design/deployment limits; 9-10 = exceptional robustness or scope discipline for the dimension. These dimensions are separate judgments; they should not be averaged into a venue verdict.

## Claim-by-claim judgment

### C1 - yes: Two tangent-residual ridge updates target cosine-relevant direction and collapse into one affine document map, retaining native destination queries.

**Current text:** abstract; introduction contributions; method equations (2)-(9); conclusion.

**Positive evidence.** The tangent target r[y-(u y^T)u] is orthogonal to the current unit prediction u and equals -r^2 times the cosine-loss gradient for nonzero predictions. Each fitted update is affine, so accumulating B0+Delta0+Delta1 yields one final coefficient matrix. The source implementation uses lambda=10, exactly two float64 updates, and float32 output coefficients. The stored second correction is absorbed into B2; inference applies affine multiplication and row normalization. A fitted shared correction need not itself remain tangent, and the paper explicitly says so.

**Scope.** Algebra and implementation support the computation, not guaranteed finite-step cosine improvement, universal retrieval improvement or an independently verified novelty claim. The scale-equivariance statement requires common positive scaling and nonzero predictions, as stated.

**Strongest supported wording.** ARC2 is a two-update, direction-targeted refinement with one affine-plus-normalization document application stage and unchanged destination queries.

**Precise sources:** `src/arc2_global/model.py::_tangent2;transform_old_docs`; `src/arc2_global/solver_backend.py::tangent2_primal`; `paper/sections/method.tex::equations (4)-(8)`.

### C2 - yes: At matched 1,024-pair fitting exposure, ARC2 has the highest development macro nDCG among six declared adapters.

**Current text:** abstract; introduction; results 5.1; generated/dev_macro.tex.

**Positive evidence.** Equal-condition means recomputed from summary.means: ARC2 0.527477527300496; Procrustes 0.5031524182600609; LA2M 0.42342257351929274; SimpleLinear 0.3553776623832738; ridge 0.4318244780276741; Converter 0.36631519310915556. ARC2-minus-Procrustes is 0.024325109040435233, family interval [0.018132175212397208,0.030791640313948616]. All five saved development macro family intervals are positive. Existing per-query arrays reproduce all 160 mean rows to max absolute error 9.44e-16.

**Scope.** Four inspected development collections, two encoder pairs, three budgets, five fixed seeds; intervals do not remove method selection and do not imply general-population superiority. The statement concerns declared baseline configurations.

**Strongest supported wording.** Across the 24 fixed-supervision development conditions, ARC2 has the largest six-adapter macro nDCG, with positive five-comparison family intervals against each baseline.

**Precise sources:** `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json::means;aggregate_contrasts`; `results/b1c_r3_review_20261031/evidence/run/scoring/cell_index.json`; `results/b1c_r3_review_20261031/evidence/run/scoring/per_query_{FiQA,NanoNQ,NanoHotpotQA,NanoFEVER}.npy`.

### C3 - yes: The development gain is broad in nDCG, while Recall and native references constrain its interpretation.

**Current text:** results 5.1; discussion.

**Positive evidence.** Each of four collection-level nDCG macros favors ARC2 over all five baselines. Point gains over Procrustes occur in 23/24 conditions, and over each other baseline in 24/24. Encoder-specific Procrustes gains are 0.025732936236754725 and 0.02291728184411574. ARC2 macro Recall 0.8658612474562474 is slightly below Procrustes 0.8660998378473379; difference -0.0002385903910903914 has descriptive interval [-0.004943626172438673,0.0043358499949124945]. All 24 ARC2 partial-development nDCG means are below native Full-X.

**Scope.** Collection and condition comparisons are descriptive; no claim of 24 significant improvements or Recall superiority follows. Full-X uses source queries, so its practical availability depends on the stated destination-query requirement.

**Strongest supported wording.** Development gains concern macro top-ranked relevance across the measured conditions, with one Procrustes point loss, no macro Recall advantage over Procrustes, and a viable native incumbent alternative when source queries remain acceptable.

**Precise sources:** `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json::means;condition_contrasts;aggregate_contrasts`; `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json::per_encoder_macro`.

### C4 - yes: The second correction adds measurable development value; the ridge and lambda controls have the reported limited interpretation.

**Current text:** abstract; introduction; results 5.2; generated/ablation.tex.

**Positive evidence.** Two-minus-one macro nDCG is 0.006923862939737235 with separate-family interval [0.003809388309482942,0.009959126205904258]. Per-query recomputation confirms 22/24 positive condition means and all seed macros positive: 17=0.003827292446927389,29=0.006180850754361864,41=0.007927119071210907,53=0.007647106742974317,67=0.00903694568321168. ARC2-minus-affine-ridge is 0.09565304927282199 with ablation-family interval [0.07535298921225946,0.11663127039230592]. Lambda1-minus10 is +0.0031974956912717346, interval [-0.0018903844098364442,0.00830403326634241]; lambda100-minus10 is -0.00925533869678723, interval [-0.01321398029023485,-0.005510245768211927].

**Scope.** This is DEV mechanism evidence, not prospective proof that two steps are necessary on TREC or that lambda10 is optimal. Ridge comparison changes both directional targets and retained prior, as the paper states. The two nonpositive second-step conditions are FiQA/E5 50% and 75%.

**Strongest supported wording.** A second update adds a repeatable bounded development nDCG benefit without another document inference stage; the controls support the tested initialized refinement, not an isolated universal tangent mechanism or an optimum step count.

**Precise sources:** `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json::overall_macro`; `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/{FiQA,NanoNQ,NanoHotpotQA,NanoFEVER}/cell_index.json`; `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/{FiQA,NanoNQ,NanoHotpotQA,NanoFEVER}/per_query.npy`; `protocols/B1M_B1P0_DEVELOPMENT_20261026.md`.

### C5 - yes: The held TREC-COVID study is a prospective fixed-procedure, matched-budget confirmation within this project.

**Current text:** experimental setup; results 5.3.

**Positive evidence.** Protocol fixes the full 171,332-document/50-query collection, two pairs, five seeds, six methods, three budgets and 30 contrasts. Current lock hash matches all sealed references. Ranking seal is dated 2026-10-31T19:56:09.382605Z; separate verification completes 20:11:42.810083Z with 184/184 ordered top100 matches and qrels_opened=false; first-final-open receipt is 20:12:17.410541Z. All 184 local raw ranking hashes match the seal. The source scorer verifies the seals and writes the receipt before label acquisition.

**Scope.** I verified the recorded chain and file hashes, not remote execution, complete organizational exposure history, inaccessible endpoints or a cryptographic proof that nobody had seen public benchmark labels. Independent refers to held-collection confirmation, not cross-family reviewer independence.

**Strongest supported wording.** The recorded B2 protocol, seal and separate-verifier chain supports a prospectively frozen held-collection evaluation in this project, conditional on the recorded non-exposure and execution provenance.

**Precise sources:** `protocols/B2_TREC_COVID_CONFIRMATION_20261031.md`; `configs/b2_lock.json`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/metadata.json`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/ranking_seal.json`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/verification/verification_seal.json`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/first_final_qrel_open.json`; `ops/b2_score.py`.

### C6 - yes: On TREC/E5, gains over the evaluated Converter and ridge persist at all three matched budgets; eleven total family-supported contrasts are reported.

**Current text:** abstract; introduction; results 5.3; conclusion; generated/trec_means.tex; generated/trec_family.tex.

**Positive evidence.** E5 Converter differences at 25/50/75% are 0.25723359077319435,0.23138457517015265,0.1999540966512042, with respective family intervals [0.17573076152800798,0.33756850203860655], [0.15671745879653792,0.3085072832020045], [0.13925018639424472,0.2642221645268023]. E5 ridge differences are 0.2641805555881269,0.2622674417365517,0.2819970458539894, all positive family intervals. Across both pairs: five supported Converter improvements, four ridge, two SimpleLinear; 11 positive/19 unresolved/0 negative family intervals. All 40 mean rows reproduce from per-query arrays to max error 5.56e-16; all 30 saved nDCG-family quantiles reproduce exactly from saved bootstrap draws.

**Scope.** One held collection with 50 independent queries, two fixed pairs, five averaged mapping seeds. Positive family outcomes concern declared adaptations. There is no prospective all-baseline dominance or independent second-step confirmation.

**Strongest supported wording.** On the prospective TREC/E5 evaluation, ARC2 improves nDCG over the declared Converter and ridge at all three matched budgets under the locked 30-contrast family; additional supported contrasts yield eleven total.

**Precise sources:** `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json::means;contrasts;bootstrap`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/per_query.npy`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/bootstrap_draws.npy`.

### C7 - yes: TREC geometric baselines remain competitive; ARC2 has no confirmed nDCG superiority over Procrustes or LA2M.

**Current text:** results 5.3; discussion; generated/trec_means.tex; generated/trec_family.tex.

**Positive evidence.** All six ARC2-minus-Procrustes point differences are negative; MiniLM/75% is -0.000023564924613148544. Every Procrustes and LA2M nDCG family interval crosses zero. The current table ranks unrounded adapter means and does not put superiority markers on those comparisons.

**Scope.** Unresolved is not equivalence or noninferiority. This limits the added held-collection evidence for the angular refinement beyond geometric alignment, but does not contradict the narrower E5-versus-Converter/ridge claim.

**Strongest supported wording.** Procrustes is numerically ahead in all six held nDCG cells, and the family cannot distinguish ARC2 from Procrustes or LA2M; the confirmed held gains concern other stated configurations.

**Precise sources:** `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json::contrasts;means`.

### C8 - yes: MiniLM/75% is close in nDCG to native Full-Y and has the largest adapter Recall point mean at every TREC budget.

**Current text:** abstract; results 5.3; generated/trec_recall.tex; prospective figure.

**Positive evidence.** MiniLM/75% ARC2 nDCG is 0.519513052034007 versus Full-Y 0.5202728348242263, an observed gap -0.0007597827902193; 25% of rows remain proxies. MiniLM ARC2 Recall point means 0.08963088480259038,0.09529158965710632,0.09983604059514704 exceed all five adapter alternatives at corresponding budgets. Full-Y Recall is 0.10521378018323918. E5 ARC2/75% Recall is 0.09966692928143464 versus Full-Y 0.11624395516879528.

**Scope.** Recall is auxiliary/descriptive; no family-adjusted superiority, native-quality equivalence or coverage preservation claim. Point nDCG proximity does not establish equivalence. The paper states this distinction.

**Strongest supported wording.** MiniLM ARC2 at 75% has observed nDCG near the native destination reference while keeping one-quarter proxy rows, and leads the six-adapter Recall point means at the three measured budgets.

**Precise sources:** `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json::means`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/per_query.npy`.

### C9 - yes: Across all five collections, E5 ARC2 at 25% exceeds the measured Converter and ridge at 75%.

**Current text:** abstract; introduction; results 5.4; generated/budget_leverage.tex; conclusion.

**Positive evidence.** ARC2/25%, Converter/75%, ridge/75% nDCG triples: FiQA=(0.27310684220470094,0.2095336751807801,0.1609714907578672); NanoNQ=(0.5071236847804641,0.40208721230157407,0.44284099940693855); NanoHotpotQA=(0.5844856557302884,0.5016332374347163,0.5053470075849882); NanoFEVER=(0.7554512732607813,0.7325762381767909,0.7289860142730652); TREC=(0.562801573213321,0.40982778236858286,0.3277848331657977). All ten point differences are positive.

**Scope.** Post-hoc descriptive comparison of the measured grid, not a member of matched-budget families. It shows lower logical destination-vector exposure, not the minimum budget for equal quality, threefold physical savings, or superiority over 25% Procrustes/LA2M. The table retains these alternatives and native references.

**Strongest supported wording.** At the measured E5 operating points, ARC2/25% has larger mean nDCG than the evaluated Converter and ridge/75% on each of five collections; this is a descriptive quality-exposure observation.

**Precise sources:** `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json::means`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json::means`.

### C10 - yes: Using all already-paid FiQA pairs strengthens MiniLM at the same 50% destination-document budget, with important E5 and cross-regime limits.

**Current text:** introduction; results 5.5; generated/allpaid.tex; discussion.

**Positive evidence.** MiniLM ARC2 changes from 0.3075048582716371 to 0.36714602143626507, delta 0.05964116316462802 with 32-family interval [0.03934110686868015,0.08060437708604837]. Its all-paid comparisons beat Procrustes, LA2M, SimpleLinear and Converter; ridge is unresolved with delta -0.00011725527452398765. E5 all-paid ARC2 trails Procrustes and LA2M with negative family intervals, beats SimpleLinear and ridge, and is unresolved against Converter. Its allpaid-minus-fixed delta -0.019768225474924635 has interval [-0.056329874306672884,0.016636927373489714]. Fixed MiniLM ARC2 trails every all-paid baseline in the cross-regime family. All 28 mean rows reproduce to max error 1.00e-15 from existing per-query arrays.

**Scope.** FiQA DEV, one 50% set of 28,819 paid pairs, not held confirmation or zero additional fitting work. This comparison retains summed-objective lambda10 and uses dual fixed rankings versus primal all-paid fits; the current paper discloses both. It does not isolate data quantity at fixed effective regularization.

**Strongest supported wording.** For the fixed recorded procedure on FiQA/MiniLM, fitting all paid pairs improves nDCG without additional destination-document exposure; the result is encoder-dependent and does not establish an all-paid universal winner.

**Precise sources:** `results/b1p_r5_review_20261027/scoring/results_summary.json::means;contrasts`; `results/b1p_r5_review_20261027/scoring/per_query.npy`; `protocols/B1P_ALL_PAID_FIQA_20261026.md`; `src/arc2_global/solver_backend.py`.

### C11 - yes: Inserting native vectors can improve or damage the same fitted map, so mixed-gallery relevance must be measured.

**Current text:** introduction motivation/contribution; results 5.5; conclusion.

**Positive evidence.** Five-seed all-paid ARC2 MiniLM proxy-only to mixed nDCG is 0.3509507352060274 -> 0.36714602143626507; E5 is 0.31490775036459107 -> 0.29186698206096207. E5 Recall changes 0.6541642457542457 -> 0.5594899234099234, and top10 paid share 0.49164 -> 0.06472000000000001 despite 50% paid coverage. These are within-fit before/after replacement diagnostics, not different fitted models.

**Scope.** Descriptive development evidence; pure endpoint already trained on paid pairs and is not a zero-encoding deployment. Returned-share imbalance does not identify a unique causal mechanism or establish miscalibration. Current prose does not make that stronger assertion.

**Strongest supported wording.** For these fixed fitted galleries, paid-vector insertion changes judged retrieval in opposite directions across the two pairs; proxy-only quality cannot substitute for evaluation of the mixed gallery to be searched.

**Precise sources:** `results/b1g_r1_review_20261027/scoring/results_summary.json::aggregate_five_seed_conditions;case_diagnostics_and_metrics`; `protocols/B1G_MIXED_GALLERY_DIAGNOSTICS_20261027.md`.

### C12 - yes: The final adapter is compact in coefficient storage and avoids neural mapper training; exposure and storage are distinct from physical deployment cost.

**Current text:** abstract; method 3.5; discussion; conclusion.

**Positive evidence.** (384+1)*768=295,680 float32 coefficients=1,182,720 bytes=1.1279296875 MiB. Converter architecture widths (384,3840,3840,3840,768) give 33,927,168 weights/biases=135,708,672 float32 bytes, ratio 114.74285714285715. Source implements affine ridge solves and no neural training for ARC2. Both dual and primal backends implement the same exact-arithmetic equations with distinct stated complexity. Paid exposure counts anchors in |A union S|; B2 paid counts are 42,833/85,666/128,499.

**Scope.** Parameter bytes exclude fitting state, galleries, encoder weights and deployment memory. Primal/dual finite-precision rankings can differ. Cached full-destination evaluation does not measure partial physical encoding work, end-to-end migration saving, latency, ANN behavior or SLOs. Affine ridge has identical coefficient storage, as stated.

**Strongest supported wording.** ARC2 stores a 1.13 MiB final affine coefficient matrix, 114.7 times smaller in float32 parameter bytes than the evaluated Converter; its demonstrated efficiency quantities are structural storage and logical exposure, not measured deployment savings.

**Precise sources:** `src/arc2_global/model.py`; `src/arc2_global/solver_backend.py`; `src/arc2_global/embedding_converter.py::parameter_count;build_model`; `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/ranking_seal.json::cells`; `paper/sections/method.tex::Computation and Storage`.

## What is actually missing

**Current-claim necessities: none identified.** No new experiment is necessary to retain the exact bounded claims reviewed here. The absence of a universal best-method win, independently confirmed second-step necessity or a physical deployment study is already reflected in the manuscript and is not grounds to relabel these narrower claims unsupported.

**Useful optional extensions:**

- More independent collections and migration pairs: Broader robustness and transfer; not required to sustain the specified DEV and TREC results.
- Prospectively locked one-versus-two-step controls on fresh held data: Independent necessity/value of the second correction beyond geometric alignment; current second-step claim is explicitly DEV.
- Additional paired-document-only baseline sensitivity and stronger/localized adapters: Robustness to implementation/training-policy choices or a broader method-ranking claim; current claim is restricted to the declared configurations.
- A physical incremental migration/index/serving measurement under a concrete deployment: Latency, resource, ANN/SLO and monetary/end-to-end savings claims; none is claimed here.
- Denser budget grid or prospectively defined quality-matching analysis: The minimum exposure at a target quality; current 25-versus-75 comparison is descriptive.

The paper says an anonymous public evidence/code link is pending. Providing accessible frozen artifacts would improve reader reproducibility and submission completeness; it does not require rerunning or revising the supported scientific outcomes.

## Audit boundaries and prior-opinion disclosure

Existing arrays reproduce all 160 DEV, 40 TREC and 28 all-paid mean rows within 1.0e-15. The second-step consistency, all ten cross-budget point signs, parameter arithmetic and B2 saved family quantiles were recomputed read-only. All 184 B2 ranking hashes match the recorded seal. The recorded ranking seal, separate verification and first-label-open receipt have the stated order. These checks are narrower than rerunning the scientific pipeline.

- No qrel file was opened, parsed or scored. Metric correctness against labels was not independently recalculated.
- No new fit, retrieval, bootstrap sampling, experiment, source/manuscript edit or publication occurred. Only the two requested reports were written in the workspace; PDF review images were temporary outside it.
- No full remote cache, fitting-checkpoint, encoder regeneration or physical endpoint replay was performed. The existing verifier record was inspected.
- The complete no-prior-label-exposure history is not independently proved; conclusions rely on recorded prospective provenance.
- No external literature/novelty/citation correctness audit, original-paper reproduction certification, isolated timing measurement or deployment audit.
- Input hashes describe bytes examined, not proof of scientific correctness or exposure independence.

**Disclosure:** Reading required workspace AGENTS.md exposed earlier audit verdicts, an earlier score mention and reviewer interpretations. The B2 protocol also contains a prior D1 characterization. None was used as evidence or a score anchor. No earlier standalone score/review report or author-summary file was read. This is a fresh re-evaluation from current claims/raw records, but cannot be described as entirely opinion-unexposed.

**No gate was advanced.** This report does not alter any historical verdict, release a protocol STOP, authorize an experiment or establish cross-family independent review.

## Exact current input identities

The JSON companion contains the complete exact-byte SHA256 manifest for **245** examined inputs, including every inspected raw B2 ranking. Manifest digest (canonical compact JSON of the ordered `input_hashes` array): `64555c2f0a3cc42fa55592b96ecdad2a059a4552061ae3b7c2dfd2c178903741`. No qrel content is included in that manifest.

| Primary input | SHA256 |
|---|---|
| `paper/ARC2_Global_DASFAA2027_final.pdf` | `e91b71e929a25d9a6e6a94d0f95703fa9eefbc80e8ef12d53082c1a2a82f85bc` |
| `paper/review/scoring_20261102/EVIDENCE_PRECHECK.json` | `bee8d16ee1523a428a9db77df99b3666836889f6a275668bc46b6945701e6415` |
| `results/b1c_r3_review_20261031/evidence/run/scoring/summary.json` | `501f065498d7325d402fcf2eef616b1d4b602ecf91d042d9ac03f780f597fec5` |
| `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/scoring/summary.json` | `646b1f535db1138dc51a2d8d1296b97de89ba8354ead9f88e45080c9cb5f18c7` |
| `results/b1mp0_r1_review_20261026/b1m_full_r1_20261026/scoring_r2_binary/results_summary.json` | `688d8b07a91b952f7ef96e859c5daa08cae4122c8ee69ae8dccf64dbe351eded` |
| `results/b1p_r5_review_20261027/scoring/results_summary.json` | `3ba283b580f6a7b2704a4c6746243987a9056c852e8e7f71ef78399984418fe7` |
| `results/b1g_r1_review_20261027/scoring/results_summary.json` | `2b5dbab47bb470bb546ef79a3c591144c9093d0090c7cc7b2eace416353df70f` |
| `configs/b2_lock.json` | `e00c970a4061ce6d50f2af9817621243959a9372e6c12a0d4e9c9c9c9d2a93f5` |
| `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/ranking_seal.json` | `08e82c19a2d1974edb094e520d0b1b6ac4e6138e3a717c5014d183669c7c25de` |
| `results/b2_review_20261101/evidence/results/b2_full_r1_20261031t064859/verification/verification_seal.json` | `78e67ab2aac47d0590db54ffd20170c30f8e7a5c96153bf17a1fee1e5322c968` |

Generated at 2026-11-01T19:32:54.071595+00:00. Model gpt-6.1-sol/high; review_independence=same-family; acceptance_status=provisional.
