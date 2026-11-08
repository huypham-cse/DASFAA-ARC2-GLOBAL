# Citation audit: `nanobeir`

**Decision: KEEP.** Existence verified as a provider-maintained dataset collection, not a formal paper. Confidence: high for resource identity and citation relevance; medium-high for the resource year. This is a same-family/provisional audit by GPT-6.1-Sol, not independent cross-family verification.

## Metadata

- Provider/author: **Zeta Alpha**, whose official Hugging Face organization is `zeta-alpha-ai`.
- Title: **NanoBEIR**; the collection displays “NanoBEIR 🍺”. Omitting the decorative emoji is harmless.
- Type: Hugging Face dataset collection; the current `@misc` entry is appropriate. No paper, venue, DOI, or individual authors are established or needed.
- Year: **2024** is supported as the constituent datasets' creation year. Live provider API responses give NanoNQ `createdAt=2024-09-10T09:44:18.000Z`, NanoHotpotQA `2024-09-10T09:43:58.000Z`, and NanoFEVER `2024-09-10T09:43:44.000Z`. These are not proof of the collection object's exact creation date or a formal publication date.
- URL resolves to the relevant collection. Access note matches this audit's date, 1 November 2026.

## Live primary sources

1. [Official NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir): identifies smaller BEIR versions with 50 queries and at most 10,000 documents per dataset; lists NanoNQ, NanoHotpotQA, and NanoFEVER under the provider organization.
2. [Official provider organization](https://huggingface.co/zeta-alpha-ai): displays the name Zeta Alpha and its NanoBEIR collection.
3. [NanoNQ API](https://huggingface.co/api/datasets/zeta-alpha-ai/NanoNQ): live GET returned identifier `zeta-alpha-ai/NanoNQ`, author `zeta-alpha-ai`, the creation timestamp above, and current SHA `77540146379abf95df8326a3c5bb9eb21c7146c3`.
4. [NanoHotpotQA API](https://huggingface.co/api/datasets/zeta-alpha-ai/NanoHotpotQA): live GET returned identifier `zeta-alpha-ai/NanoHotpotQA`, author `zeta-alpha-ai`, the creation timestamp above, and current SHA `d79c0cdda980aba54842756770928035e1b61a51`.
5. [NanoFEVER API](https://huggingface.co/api/datasets/zeta-alpha-ai/NanoFEVER): live GET returned identifier `zeta-alpha-ai/NanoFEVER`, author `zeta-alpha-ai`, the creation timestamp above, and current SHA `a8bfdf1bf15181167a7e22e69cf8754bdea9b4c8`.

The collection and organization were opened with the web tool. Its API opens failed; direct live HTTP GETs using PowerShell `Invoke-RestMethod` succeeded for all three provider API URLs. Current API SHAs establish what was consulted, not the revisions used in the authors' experiments. No cached source or prior review was needed.

## Uses

| File / line | Verdict | Reason |
|---|---|---|
| `sections/experimental-setup.tex:13` | SUPPORTS | NanoNQ, NanoHotpotQA, and NanoFEVER are listed components of this smaller-BEIR collection. The citation supports their provenance and small-dataset description. The manuscript's precise document counts, chosen development role, encodings, and label-handling chronology remain claims about its pinned experiments; this resource citation neither verifies nor contradicts them. FiQA is jointly attributed with BEIR and is not assumed to be NanoFiQA2018. |
| `sections/related-work.tex:30` | SUPPORTS | The provider describes reduced BEIR datasets, supporting the statement that NanoBEIR offers smaller collections. “Suitable for development comparisons” is the authors' reasonable usage inference, not a claim of independent validation by the provider. |

## Fix

None required. Retain the resource citation and the present 2024 year; interpret that year as the dataset release/creation year supported above. Do not promote it to a formal-paper citation. Exact experiment counts require pinned local manifests and are outside this citation audit; no current dataset row totals were used to certify them.
