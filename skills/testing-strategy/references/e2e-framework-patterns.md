# E2E Framework Patterns: Playwright and Cypress

## Playwright: CI Configuration

### Parallel sharding (recommended for suites > 5 min)

```yaml
# .github/workflows/playwright.yml
strategy:
  matrix:
    shard: [1/4, 2/4, 3/4, 4/4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}
```

### API mocking with route.fulfill

```typescript
test('shows error on API failure', async ({ page }) => {
  await page.route('**/api/users', route =>
    route.fulfill({ status: 503, body: 'Service Unavailable' })
  );
  await page.goto('/users');
  await expect(page.getByText('Unable to load users')).toBeVisible();
});
```

### Multi-tab pattern

```typescript
test('opens in new tab and syncs state', async ({ context }) => {
  const page1 = await context.newPage();
  const page2 = await context.newPage();
  await page1.goto('/dashboard');
  await page1.click('[data-testid="open-in-new-tab"]');
  // Both pages share the same browser context (cookies, localStorage)
  await expect(page2.getByText('Dashboard')).toBeVisible();
});
```

### waitForSelector vs. sleep

```typescript
// WRONG — will race on slow CI
await page.click('#submit');
await page.waitForTimeout(2000); // sleep
await expect(page.getByText('Success')).toBeVisible();

// RIGHT — deterministic
await page.click('#submit');
await page.waitForSelector('[data-testid="success-message"]');
// or: await expect(page.getByText('Success')).toBeVisible(); // has built-in retry
```

---

## Cypress: CI Configuration

### Parallelism via Cypress Cloud

```yaml
# .github/workflows/cypress.yml
- name: Cypress run
  uses: cypress-io/github-action@v6
  with:
    record: true
    parallel: true
    group: 'CI'
  env:
    CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
```

### API interception

```javascript
cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers');
cy.visit('/users');
cy.wait('@getUsers');
cy.get('[data-testid="user-list"]').should('have.length', 3);
```

### Avoiding sleep in Cypress

```javascript
// WRONG
cy.click('#submit');
cy.wait(3000); // arbitrary sleep
cy.get('.success').should('be.visible');

// RIGHT
cy.click('#submit');
cy.get('.success', { timeout: 10000 }).should('be.visible');
// Cypress retries the assertion; no sleep needed
```

---

## Choosing Between Them: Non-Obvious Factors

**Playwright wins for**:
- Multi-browser matrix (Firefox, WebKit) required by regulatory or accessibility requirement
- Testing browser extensions or chrome:// pages
- Testing flows that open multiple tabs (OAuth popups, PDF viewers, print dialogs)
- Systems where network traces (HAR) are needed for debugging
- Teams that will exceed the Cypress free tier on CI run minutes

**Cypress wins for**:
- Teams that need interactive time-travel debugging during test authoring (the Cypress UI is genuinely superior for this)
- Projects with existing Cypress investment and Chrome-only requirement
- React/Vue component testing when Cypress's component testing runner is already in use
- Teams that find Playwright's async/await model more cognitive overhead than they want

**Never decide based on**: syntax preference, GitHub stars, "everyone uses X." Decide based on which framework's failure modes match your team's acceptable costs.

---

## MSW (Mock Service Worker) for Shared Mocking

MSW works in both browser and Node.js, making it the right tool for sharing mock definitions between unit, integration, and E2E layers:

```typescript
// handlers.ts — shared across all test layers
export const handlers = [
  http.get('/api/users', () =>
    HttpResponse.json([{ id: 1, name: 'Alice' }])
  ),
];

// unit/integration: setupServer from msw/node
// browser/E2E: setupWorker from msw/browser
```

This pattern eliminates the drift problem where unit test mocks and E2E mocks describe different contracts for the same endpoint.
