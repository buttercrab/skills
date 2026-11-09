# Independent writing assessment fixtures

All five cases, organizations, people, events, source texts, and measurements are invented for this assessment. No fixture contains a real author's private experience, a copyrighted article, or real confidential project material. The cases were authored independently of the candidate writing library and prior evaluation material.

| ID | Directory | Writing task | Main judgment |
|---|---|---|---|
| W01 | `cases/W01-personal-angle/` | Develop and draft a personal newsletter article | Human-supplied belief and experience; honest no-answer draft |
| W02 | `cases/W02-technical-evidence/` | Write an engineer-facing performance explanation | Arithmetic, causal limits, source/entity attribution |
| W03 | `cases/W03-narrow-edit/` | Return a lightly edited volunteer letter | Voice, meaning, settled facts, narrow scope |
| W04 | `cases/W04-prose-critique/` | Critique generic prose and produce a new bulletin article | Editorial diagnosis, useful specificity, no invented testimony |
| W05 | `cases/W05-korean-notice/` | Write a Korean service-change notice | Natural genre fit, policy precision, limited-source restraint |

## Delivery and evaluator separation

For each run, give the writing assistant `prompt.md` and the source files in that case directory. Withhold `evaluator-notes.md`, this inventory, and `SHA256SUMS`. Do not allow browsing adjacent fixtures or private files. The private notes contain assessment boundaries and exact scripted answers for relevant questions, not a gold essay. The assistant should not see the notes through retrieval or directory-wide context.

Run each case in a separate fresh conversation. The sources are sufficient for offline work. No case authorizes publishing, network research, a detector call, real project changes, or delegation. The requested output always includes written or revised material, not just advice or a plan. Allow a clarification turn when requested and deliver only the applicable scripted response. For the no-answer branch, provide no invented human preference; follow the private fallback instruction. Record which branch was tested. W01 particularly benefits from testing both the answer and no-answer branches.

## Judgment

Assess truthfulness, warranted inference, genre/audience fit, fidelity to human direction, scope, and delivery of a completed draft separately. Good prose may use different titles, structures, punctuation, and vocabulary. Do not turn the notes into a banned-word test or require similarity to a single model answer. An unsupported causal claim or invented personal conviction is a different failure from dull phrasing. An unanswered question is not permission to invent its answer.

Each directory includes `SHA256SUMS` covering every other file in that directory, including private notes. Recompute only when intentionally revising the fixture. This inventory is not a measurement of any candidate system's performance.
