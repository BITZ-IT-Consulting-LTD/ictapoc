import { test, expect } from '@playwright/test';

test.describe('Authentication E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the login page before each test
    await page.goto('http://localhost:80/login');
  });

  test('should allow a user to log in successfully and redirect to dashboard', async ({ page }) => {
    // Fill in the login form
    await page.fill('input[type="text"]', 'nmbajah');
    await page.fill('input[type="password"]', 'Starten1');

    // Click the login button
    await page.click('button[type="submit"]');

    // Expect to be redirected to the dashboard
    await expect(page).toHaveURL('http://localhost:80/dashboard');
    await expect(page.locator('h1')).toHaveText('Dashboard');
    await expect(page.locator('p')).toContainText('Welcome, nmbajah! Your role is: admin');
  });

  test('should display an error message for invalid login credentials', async ({ page }) => {
    // Fill in the login form with invalid credentials
    await page.fill('input[type="text"]', 'invaliduser');
    await page.fill('input[type="password"]', 'invalidpass');

    // Click the login button
    await page.click('button[type="submit"]');

    // Expect to stay on the login page and see an error (assuming an alert or similar)
    await expect(page).toHaveURL('http://localhost:80/login');
    // This part would depend on how your app displays login errors.
    // For now, we'll just check if the dashboard is NOT visible.
    await expect(page.locator('h1')).not.toHaveText('Dashboard');
  });

  test('should log out a user and redirect to login page', async ({ page }) => {
    // First, log in successfully
    await page.fill('input[type="text"]', 'nmbajah');
    await page.fill('input[type="password"]', 'Starten1');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('http://localhost:80/dashboard');

    // Click the logout button (assuming there is one in the App.vue header)
    // This requires adding a logout button to App.vue
    // For now, we'll simulate direct navigation to login after clearing local storage
    await page.evaluate(() => {
      localStorage.clear();
    });
    await page.goto('http://localhost:80/dashboard'); // Try to go to a protected route
    await expect(page).toHaveURL('http://localhost:80/login'); // Should be redirected to login
  });

  // Note: Testing token refresh in E2E is more complex as it requires
  // simulating token expiration and subsequent API calls.
  // This would typically involve more advanced mocking or waiting for specific network requests.
  // For a stub, we'll leave it as a comment.
  test('should refresh token automatically when access token expires', async ({ page }) => {
    // This test would involve:
    // 1. Logging in to get tokens.
    // 2. Manipulating localStorage to set an expired access token but a valid refresh token.
    // 3. Making an API request that would trigger the interceptor.
    // 4. Asserting that the API request succeeds and a new access token is stored.
    test.skip('Advanced token refresh test needs implementation');
  });
});
