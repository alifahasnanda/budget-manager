# Design rationale

I separated the project into layers: models (schema), validation (rules),
services (calculations), storage (files) and cli (terminal input/output).
All validation lives in one function, validate_row(), which is used at every
entry point: the add command, CSV import and loading the saved file. Unknown
categories are rejected with a clear message instead of being changed to
"other", because silently correcting data would hide mistakes in the user's
budget. Trade-off: the user must use one of the allowed categories.