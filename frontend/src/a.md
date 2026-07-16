## 9. Improve Mission Control

Show missions as rows:

```text
○ Finish heatmap                  HIGH
✓ Connect Hackatime               DONE
○ Prepare project demo            MEDIUM
```

Every mission should show:

- Completion button
- Mission name
- Priority
- Due date
- Edit button
- Delete button

Also add:

- All, Active, and Completed filters
- A mission count
- A confirmation before deleting
- A line through completed missions
- A message when there are no missions
- Smaller buttons
- Clear priority colors

Use red only for delete or urgent missions.

## 10. Improve Mission Forge

Use one main form instead of several large boxes.

Fields:

- Mission name
- Description
- Priority
- Due date
- Create Mission button

Add:

- Visible labels above every field
- Error text below incorrect fields
- A disabled button while saving
- “Creating…” while the request runs
- A success message
- A small mission preview
- Consistent input sizes
- A character limit for long descriptions

Example preview:

```text
MISSION PREVIEW

Finish the coding heatmap
High priority · Due Friday
```

## 11. Improve Coding Intelligence

Use this order:

1. Page heading
2. Today’s coding goal
3. Seven-day heatmap
4. Projects
5. Languages
6. Hackatime connection

Rename “Status Bar” to:

```text
Today's Coding Goal
```

Show:

```text
42 minutes of 4 hours
18% complete
```

Add a progress bar:

```css
.progress {
  width: 100%;
  height: 8px;
  overflow: hidden;
  background: #202c3c;
  border-radius: 999px;
}

.progress-fill {
  height: 100%;
  background: #38bdf8;
  border-radius: inherit;
}
```

Do not show `0%` when the API fails. Show:

```text
Coding activity could not be loaded.
```

## 12. Improve the heatmap

Add:

- Seven equal cells
- Weekday names
- Hours for every day
- A Less-to-More legend
- Exact information when hovering
- A border around today
- Sideways scrolling on small screens
- A message when the week has no activity

Use one color family:

```css
.heat-level-0 { background: #172033; }
.heat-level-1 { background: #123f5c; }
.heat-level-2 { background: #075985; }
.heat-level-3 { background: #0284c7; }
.heat-level-4 { background: #0ea5e9; }
.heat-level-5 { background: #38bdf8; }
.heat-level-6 { background: #bae6fd; }
```

## 13. Improve the projects card

Each project should show:

- Project name
- Time
- Percentage
- Small progress bar

Make the list scrollable:

```css
.projects-scroll {
  max-height: 320px;
  overflow-y: auto;
  padding-right: 0.5rem;
}
```

Also:

- Remove the red background.
- Use smaller project rows.
- Sort projects by coding time.
- Keep the duration aligned on the right.
- Prevent long names from leaving the card.
- Avoid giant separate boxes for every project.
- Add “No projects recorded this week” when empty.

## 14. Improve the language card

Only display three languages:

```jsx
languages.slice(0, 3)
```

Display them like this:

```text
JSX       48%
CSS       31%
Python    21%
```

Also:

- Show a progress bar for each language.
- Align the percentage on the right.
- Do not hardcode language names.
- Hide languages with zero coding time.
- Add “No language data this week” when empty.
- Make the list compact.

## 15. Improve buttons

Create three types:

```css
.button {
  padding: 0.7rem 1rem;
  border: 1px solid transparent;
  border-radius: 9px;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
}

.button-primary {
  color: #061018;
  background: #38bdf8;
}

.button-secondary {
  color: #f1f5f9;
  background: #101722;
  border-color: #26354a;
}

.button-danger {
  color: #fecaca;
  background: transparent;
  border-color: #7f1d1d;
}
```

Button rules:

- Use only one primary button in a form.
- Do not make delete the brightest button.
- Use clear text such as “Create mission.”
- Add disabled styles.
- Do not use huge buttons.
- Make buttons large enough to tap on mobile.

## 16. Improve forms

For all inputs:

```css
input,
textarea,
select {
  width: 100%;
  box-sizing: border-box;
  padding: 0.75rem;
  color: #f1f5f9;
  background: #0b111b;
  border: 1px solid #26354a;
  border-radius: 9px;
}

input:focus,
textarea:focus,
select:focus {
  outline: 2px solid rgba(56, 189, 248, 0.3);
  border-color: #38bdf8;
}
```

Also:

- Put labels above inputs.
- Leave space between fields.
- Show useful error messages.
- Keep input heights consistent.
- Do not clear the form when an error happens.
- Do not use placeholders instead of labels.

## 17. Add loading states

Use messages such as:

```text
Loading your coding activity…
Loading today’s missions…
Checking Hackatime connection…
Calculating your focus score…
```

Do not leave the page blank while loading.

## 18. Add empty states

Use messages such as:

```text
No missions yet. Create your first mission.
No coding activity was recorded today.
No projects were recorded this week.
Everything looks clear—there are no warnings.
Hackatime is not connected.
```

Empty messages should explain what happened and what the user can do next.

## 19. Add friendly error states

Do not show technical errors such as:

```text
Request failed with status code 500
```

Show:

```text
Coding activity could not be loaded.
Please try again in a moment.
```

Add a small Try Again button when useful.

## 20. Fix spacing

Use:

- `8px` between closely connected items
- `16px` between normal items
- `20px–24px` inside cards
- `32px` between sections
- `40px–48px` after page headings

Remove:

- Random negative margins
- Cards touching each other
- Text touching card edges
- Giant empty spaces
- Different padding on identical cards
- Fixed widths that break mobile screens

## 21. Make everything mobile-friendly

```css
.cards-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 800px) {
  .cards-row,
  .two-column-layout {
    grid-template-columns: 1fr;
  }

  .page {
    width: min(100% - 1rem, 1200px);
  }

  h1 {
    font-size: 2rem;
  }
}
```

Check that:

- Cards stack vertically.
- Navigation can scroll sideways.
- Heatmap can scroll sideways.
- Text does not leave the screen.
- Buttons remain easy to press.
- Projects appear above Languages.

## 22. Improve accessibility

Add:

- Visible keyboard focus
- Input labels
- Image `alt` text
- Confirmation before deleting
- Good text contrast
- Buttons instead of clickable `<div>` elements
- `aria-label` for icon-only buttons
- Large enough touch targets
- Correct heading order

```css
:focus-visible {
  outline: 2px solid #38bdf8;
  outline-offset: 3px;
}
```

## 23. Make the About page personal

Write about:

- Why you built StarkOS
- The problem it solves for you
- Why you connected Hackatime
- What you learned
- The hardest feature
- Your favorite part
- What you will build next
- Your name
- The project version

Example:

> I built StarkOS because my coding statistics, missions, and daily plans were spread across different tools. I wanted one command center that worked around my own routine.

Add:

```text
Designed and built by Srinivasa
StarkOS v1.0
```

Rewrite it in your own voice.

## 24. Add personal details

Add a few of these:

- “Good evening, Srinivasa.”
- Your real coding goal
- A “last synced” time
- Your real mission categories
- A small StarkOS version number
- An explanation for the focus score
- A personal footer
- Your favorite current project
- A custom StarkOS wordmark
- Your plans for the next version

Do not overload the app with movie quotes or effects.

## 25. Clean the CSS

Remove:

- Duplicate selectors
- Unused styles
- Test colors
- Red debug backgrounds
- Old commented code
- Repeated navigation rules
- Repeated card rules
- Classes named `.title2`, `.title3`, or `.title5`
- Rules fighting each other
- Random fixed widths

Use understandable class names:

```text
.page-title
.section-title
.card-title
.page-description
.stat-card
.mission-row
.project-row
```

## 26. Clean the JSX

Check every frontend JSX file:

- Remove unused imports.
- Remove commented experiments.
- Use one `h1` per page.
- Add stable `key` values to mapped lists.
- Handle missing API data.
- Remove hardcoded values when real values exist.
- Use clear variable names.
- Split extremely large pages into small components.
- Keep loading and error states separate.
- Fix visible spelling mistakes.

Useful components could be:

```text
PageHeader
StatCard
MissionRow
ProgressBar
EmptyState
ErrorMessage
ProjectList
LanguageList
CodingHeatmap
```

## 27. Use subtle animations

Use simple transitions:

```css
button,
.card,
nav a {
  transition:
    background-color 160ms ease,
    border-color 160ms ease,
    color 160ms ease;
}
```

Avoid:

- Cards jumping upward
- Constant flashing
- Strong pulsing
- Large glowing animations
- Slow animations
- Animating everything

## 28. Final testing

Before resubmitting:

- Open every page.
- Click every navigation link.
- Create a mission.
- Complete a mission.
- Edit and delete a mission.
- Check the Coding page.
- Verify projects scroll.
- Verify only three languages display.
- Check the heatmap.
- Disconnect and reconnect Hackatime if safe.
- Test loading states.
- Test empty states.
- Test errors.
- Test on desktop.
- Test at tablet width.
- Test at phone width.
- Check the browser console.
- Fix visible spelling mistakes.
- Remove test content.
- Deploy the latest version.
- Check the deployed site again.
- Take new screenshots.

Your best order is: fonts → background → page width → cards → navigation → headings → Command Center → Coding page → Missions → Forge → About page → mobile testing → cleanup.