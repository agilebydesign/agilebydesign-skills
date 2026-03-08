---
title: Use And and But for conditions
impact: MEDIUM
tags: step, scenario
---

## Use And and But for conditions

Use **And** for multiple system reactions to one event; use **But** for negative conditions and constraints. Applies to Initiation/Response and steps. (Merges use_and_for_multiple_reactions and use_but_for_negative_conditions.)

**DO** use And when listing multiple reactions or conditions.
- Right: "Then **System** validates payment **and** displays confirmation".
- Right: "When **User** selects **Country** and **PaymentType**; Then **System** displays form".

**DO** use But for negative conditions and constraints.
- Right: "When **User** has no **Session**; Then **System** redirects to login".
- Right: "**User** has **PaymentType** access **but** not for this **Country**".

**DO NOT** chain positives with But or use And for contrasting conditions.
- Wrong: "Then system validates but displays error" (use And for multiple outcomes, or split into separate steps).
- Wrong: "User has access and not for country" (use But for the negative).
