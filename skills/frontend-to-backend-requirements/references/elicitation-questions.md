# Elicitation Questions

Ask these before writing the requirements doc. Not all apply to every feature — use judgment.

## Feature Scoping
- What is the name of the feature/screen/flow?
- Who is the user performing this action? (role, permissions, context)
- What problem does this solve for them?
- Is this a new surface or modifying an existing one?

## Data Needs
- What information appears on screen? Walk me through it visually.
- Are any of these values derived or computed (e.g., "completion rate", "days remaining")?
- Do you need historical data or only current state?
- Is any data user-specific vs. shared across users?
- Are there items in a list? How many? Is there pagination/infinite scroll?
- Do items in a list need to link to a detail view? What does the detail need that the list doesn't?

## Relationships
- For each piece of data, is it standalone or related to something else?
  - Example: "I show a contract — do I also need the vendor attached to it? Their logo? Their contact?"
- Are there nested relationships? How deep?
- Can the same item appear in multiple contexts with different fields needed?

## Actions
- What can the user do on this screen?
- What happens immediately in the UI when they do it?
- What confirmation or feedback should they see?
- Are there actions that should be disabled or hidden for certain users/states?

## States
- What does the screen look like before data loads?
- What if there's no data? (Empty state)
- What if the data fails to load? (Error state)
- Are there partial states — e.g., some data loads fast and some slow?
- Can the user be in a state where some actions are temporarily unavailable?

## Business Rules
- Are there any rules about what's visible based on the user's role, plan tier, or account state?
- Are there date-based rules (e.g., show X only if contract is not expired)?
- Are there count-based rules (e.g., disable action if limit reached)?
- Are there any rules you're not fully sure about?

## Uncertainties
- What are you guessing at right now?
- What would you ask backend if you had five minutes with them?
- Are there any existing APIs you think might partially solve this, but you're not sure?
