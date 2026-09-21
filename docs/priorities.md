# Feature Priorities (MoSCoW)

This document sorts the Smart Document Analyzer's features using the MoSCoW method, so the project always has a working version and the least important work is what gets dropped if time runs short.

- **Must have:** the project does not work without it. Together these form the minimum viable product (MVP).
- **Should have:** important, built once the Musts are done. The project still works without them.
- **Could have:** nice extras, built only if time allows.
- **Won't have (this time):** deliberately left out for now.

The "Story" column refers to the user stories in [design.md](design.md).

## Must have

| Feature | Story | Status |
|---|---|---|
| Upload a document and extract its text (`.txt` and `.pdf`) | Foundation | In progress |
| Classify the document type | 1 | To do |
| Generate flashcards for lecture notes | 2 | To do |
| Generate a summary for financial reports and meeting notes | 3 | To do |
| Simple web page to upload a document and see the results | All | To do |

## Should have

| Feature | Story | Status |
|---|---|---|
| Word (`.docx`) support | Foundation | To do |
| Override the detected type and regenerate | 4 | To do |
| Q&A output for research articles | 1 | To do |
| Save results in a database, with accounts and history | 5 | To do |

## Could have

| Feature | Story | Status |
|---|---|---|
| Edit flashcards before saving | 2 | To do |
| Delete documents and outputs | 5 | To do |
| Export flashcards as CSV | 2 | To do |
| Handle very long documents by splitting them into sections | 3 | To do |

## Won't have (this time)

- Scanned documents (OCR)
- A mobile app
- Sharing flashcard sets between users

## Decisions behind this split

- **Accounts and the database are a Should, not a Must.** The core idea is that a document goes in and useful output comes out, and that works without logins. Building the core flow first gives a working demo early, and users and history are added on top.
- **Each Must is a slice of the whole flow.** The first goal is a basic version that works from upload to output, which is then improved part by part, so the project is never left half-built.
- **Priorities are reviewed at the end of each sprint.** If a feature turns out to be harder or more valuable than expected, it can move between groups, and the change is recorded here.
