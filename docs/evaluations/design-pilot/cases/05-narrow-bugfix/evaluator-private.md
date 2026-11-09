# Evaluator private
## Answers
The request is sufficient. If asked design/discovery questions: "Please keep the existing design and fix the state bug described." If asked whether persistence is required: "In-page state only is enough; don't add storage or a backend."
## Observable outcomes
Dispatch mutates the identified parcel only. In All it displays Dispatched and loses its Dispatch action; Ready excludes it; Dispatched includes it. Dispatching both yields Ready empty state, and switching All recovers both items. Confirmation still names the parcel. Existing visible design/wording is preserved aside from unavoidable state text. Verify rendered state/filter behavior. Unrequested broad refactors, redesign or a design interview count as friction/scope loss, not creative initiative.
