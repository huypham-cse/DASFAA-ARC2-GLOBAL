# SimpleLinear citation audit

Verdict: **KEEP**. All three axes pass. Reviewed 2026-11-01 with gpt-6.1-sol, high reasoning, as a fresh single-entry review. No other reviewer reports or prior scores were read. No experiments were run and no manuscript files were changed.

## Three axes

| Axis | Result | Finding |
|---|---|---|
| Existence | PASS | Official pinned repository files and both SimpleLinear classes exist. The GitHub API resolved the full requested revision, committed 2026-07-04T09:50:02Z. |
| Metadata | PASS | The entry clearly cites software. Its organization and descriptive title are defensible. Treat 2026 as software/access year, not publication of a separate SimpleLinear algorithm paper. The package metadata names embedding-translation 0.1.0 and Beining Yang. |
| Context | PASS | An exhaustive citation-command scan found three current uses; all support the stated software/mapper claims. |

## Actual current contexts

- `paper/sections/experimental-setup.tex:49` ? **KEEP**. The citation identifies the compared software. Architecture, batch size, loss and final-epoch policy agree with pinned code and the local declarations; the prose explicitly disclaims full original-setting reproduction.
- `paper/sections/introduction.tex:7` ? **KEEP**. The software implements neural regression, supporting the broad alternative-mapper statement.
- `paper/sections/related-work.tex:7` ? **KEEP**. The official repository provides this mapper; the README associates the repository with the authors of the preceding work.

The JSON includes each complete current citing paragraph. SimpleLinear mentions in results.tex carry local empirical comparisons rather than additional citation commands; their numerical validity is outside this citation audit.

## Architecture and policy

The [configuration schema](https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/src/embedding_translation/config/models.py) sets layer_num=4, SELU, width 512, 50 epochs, batch 4028 and no local distillation. The [strategy/model implementation](https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/src/embedding_translation/mapper/simple_linear/strategy.py) creates five linear layers for that setting, activating between them. It combines MSE with 0.5 cosine distance, runs the configured epoch count and retains the final state. The schema's early-stopping fields are unused here. The standalone model-constructor defaults differ from the mapper configuration.

`configs/baselines.json`, `src/arc2_global/baseline_adapters.py`, `ops/b1p_neural_worker.py` and the B2 protocol establish the study's selected final-50 policy and paired-only fitting. Those are implementation declarations; shared supervision, normalization and runtime adaptation do not imply reproduction of every original-paper setting. The current setup paragraph makes that distinction. This review did not re-audit execution or retrieval outcomes.

## Sources and access

- [README.md](https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/README.md) ? official pinned source, live access 2026-11-01; SHA256 `5fc828bfa341ff4b5988ff8d47efef3066530bacaf4d087f3a40e1a6cd31ee1b`.
- [pyproject.toml](https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/pyproject.toml) ? official pinned source, live access 2026-11-01; SHA256 `6db4eb263bba420d0bba5eb8ca7fcf24fe385400ff1efd9dc422cc8ed30b658b`.
- [src/embedding_translation/config/models.py](https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/src/embedding_translation/config/models.py) ? official pinned source, live access 2026-11-01; SHA256 `d26380ad82572336d15f76a0c646930df502d8ae374baa7a56c2783a5ddb7cc3`.
- [src/embedding_translation/mapper/simple_linear/strategy.py](https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/src/embedding_translation/mapper/simple_linear/strategy.py) ? official pinned source, live access 2026-11-01; SHA256 `9f22cb2c39baca27b660260c80df31da8ab6bb856160b660b5b3840c649ea821`.
- [src/embedding_translation/mapper/simple_linear/__init__.py](https://raw.githubusercontent.com/DBgroup-Edinburgh/embedding-translation/5e62baf1544264847ce3d8feeabd1ded6499b064/src/embedding_translation/mapper/simple_linear/__init__.py) ? official pinned source, live access 2026-11-01; SHA256 `2ef7f2a35501474e298e7f9d1aae8f85edacd516b4ef4c78e04efa754b6733d6`.
- [Commit API](https://api.github.com/repos/DBgroup-Edinburgh/embedding-translation/commits/5e62baf1544264847ce3d8feeabd1ded6499b064) ? direct HTTPS succeeded and resolved the full SHA.

The web tool could not open the GitHub tree or API view. Pinned raw files succeeded through both the web tool and direct HTTPS. Two guessed configuration paths returned 404; the package initializer led to the correct models.py. The input packet's prior verification label was not used as proof.

No required corrections. Optional: record an explicit access date/full SHA in the software entry, and phrase the policy as ?trained for 50 epochs, retaining the final checkpoint.?

## Input integrity

The current bibliography SHA256 matches the packet. Hashes cover the packet, bibliography, all scanned section files, and the inspected local configuration/implementation/protocol.

- `paper/review/final_review_20261101/citations/simplelinear.input.json`: `2ea24f93172c4692a18d67521c487996668800579ca864c11e5968c37cfbf321`
- `paper/references.bib`: `c04d2e03b5df17f3e6e026bd7f8e7c942905055de4174c9a45f1fddeb7941de2`
- `configs/baselines.json`: `b0be0352d174157d91a32437c6db0e3479ceb4c829ba75a5703189f19dd4a2a5`
- `src/arc2_global/baseline_adapters.py`: `c0269d631defb4ba00f09bf6def75182b988a9d4b8c719c81633c800e1189b0d`
- `ops/b1p_neural_worker.py`: `d87efe737064d9019b2dc951ec0c593040aaa9fafe80bb73e2c75155e5f8d66e`
- `protocols/B2_TREC_COVID_CONFIRMATION_20261031.md`: `109847050cd77317eee118f459e8a6e696572eb8181d46e24b9dd0752d5827c2`
- `paper/sections/abstract.tex`: `c75dc88657f9b538f314b1787e75b08f9b3864f000a0f7e8b729effbe5f7d3d4`
- `paper/sections/conclusion.tex`: `5ab2f71361be86ad2ddc5d4d21e00cc0a1ac869c900ef6546edba72be0b572b7`
- `paper/sections/discussion.tex`: `834323c766a49b3b3874b660b9e6fdad3b660e8b5d93a5afeeae0c22fea01240`
- `paper/sections/experimental-setup.tex`: `c6dfc7e773e6f448118013e5f11ec35eed6f849f7fb475bb1d690b1e07220828`
- `paper/sections/introduction.tex`: `d67c836c50b51760cb279b62c1096a4b4a3e4498fa9e6b547df72d79cc27945f`
- `paper/sections/method.tex`: `c4babc62dd94e8c6e2ccd6b921ea9d82db762ddf73df5c6efe71a3f022ce0e37`
- `paper/sections/related-work.tex`: `bb47d22e21547ef1e96f4eb3634cda7039d2d6078082bae302d6507380a2b10f`
- `paper/sections/results.tex`: `a8d76c0bc6ffcd14af3d461baf406837e3cd34a371585cd1e9754c28a64bafd3`
