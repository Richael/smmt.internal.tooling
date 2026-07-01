# A3 — Build sequences

**Goal:** stand up an email sequence and enroll a target list into it.
**Server:** `apollo`.

## Reality check

Apollo's MCP exposes `search_sequences`, `add_contacts_to_sequence`, and
`update_sequence_status` — it **adds contacts to** and **toggles** sequences. Authoring the step
cadence/copy is done in the Apollo UI. So keep the canonical sequence in
`templates/sequence.example.yaml`, build it once in-app to match, then drive enrollment via MCP.

## Steps (prompts)

> 1. *(once, in Apollo UI)* create a sequence whose steps match `templates/sequence.example.yaml`.
> 2. "Use apollo `search_sequences` to get the id of 'SaaS Marketing Leaders — Outbound v1'."
> 3. "Use apollo `search_contacts` (or the label from A1) to get the target contacts, then
>    `add_contacts_to_sequence` to enroll them — **show me the count and stop for confirmation
>    before activating**."
> 4. "After I confirm, use apollo `update_sequence_status` to set it active."

## Output

Contacts enrolled in the named sequence (visible in the Apollo UI).

## Notes

- Personalize via merge fields the sending account supports (`{{first_name}}`, `{{company}}`).
- Respect daily sending limits per mailbox; warm new mailboxes before high volume.
- Always gate activation on a human confirm — never enroll-and-send on a loop.
- Pairs with **A2** (read back the stats once it's running) and **A4** (compare it to other lanes).
