---
title: Given describes state (Pre-Condition), not actions
impact: HIGH
tags: [exploration, specification, step]
scanner: given_state
---

## Given / Pre-Condition describes state, not actions

Pre-Conditions and Given statements establish **what must be true before** the interaction — they are state assertions that set up the conditions under which the trigger can fire. They support the idea that interactions have pre-conditions: state that must exist before the exchange can happen.

**DO** use state language — what EXISTS, not what HAPPENS. Given = state/precondition. When = first action (trigger). Then = response/outcome. Pre-Condition on an epic or story describes the state required for all its children.
- Example (right): `Given **User** is logged in` (state). `Given **Session** is active` (precondition). `Given **PaymentType** is available for **Country**` (domain state).
- Example (right): `Pre-Condition: Given **User** is logged in; And **User** has an active **Session**` — state that must be true before any story in this epic can execute.

**DO** frame Given as the pre-condition that enables the trigger. The Given establishes *why* the When can happen — without this state, the interaction would not be possible.
- Example (right): `Given **User** has access to **PaymentType** in **Country**` → enables `When **User** selects **PaymentType**`. The pre-condition authorizes the action.

**DO NOT** use action verbs in Given — clicking, sending, calling, executing are When actions.
- Example (wrong): `Given user clicks button`. `Given system sends message`. `Given API is called`.
- Example (right): `Given **User** is authenticated`. `Given **Message** has been received`. `Given **API** endpoint is available`.

**DO NOT** describe UI position or navigation as state — "is on page" is navigation, not domain state.
- Example (wrong): `Given User is on PaymentDetails step`. `Given User is viewing the form`. `Given User is at Step 2`.
- Example (right): `Given **WirePayment** creation is in progress`. `Given **PaymentDetails** requires **Account** selection`.

**DO NOT** use past-tense actions in Given — "has invoked", "has clicked" smuggle actions into preconditions.
- Example (wrong): `Given Tool has invoked method`. `Given user has clicked submit`.
- Example (right): `Given **Tool** is initialized`. `Given **Form** submission is pending`.

**DO NOT** describe functionality being tested in Given — that belongs in Then (response).
- Example (wrong): `Given activity log tracks: timestamp, action_state` — this is what you're testing.
- Example (right): `Given **ActivityLog** is initialized` (precondition) → `Then **ActivityLog** captures timestamp and action_state` (response).
