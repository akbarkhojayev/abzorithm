import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();

try {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("http://localhost:5173", { waitUntil: "domcontentloaded" });
  await page.evaluate(() => {
    window.localStorage.setItem("Coding", "fake-token");
  });
  await page.reload({ waitUntil: "domcontentloaded" });
  
  // Wait for profile icon
  await page.waitForSelector(".userIcon", { timeout: 5000 });
  await page.waitForTimeout(500);
  
  // Screenshot before click
  await page.screenshot({ path: "/tmp/new_before.png" });
  console.log("✓ Before click screenshot");
  
  // Click profile icon
  await page.$eval(".userIcon", el => el.click());
  await page.waitForTimeout(500);
  
  // Screenshot after click
  await page.screenshot({ path: "/tmp/new_after.png" });
  console.log("✓ After click screenshot");
  
  // Check if dropdown is visible
  const dropdownVisible = await page.evaluate(() => {
    const dropdown = document.querySelector(".profile-dropdown");
    return dropdown !== null;
  });
  
  console.log(dropdownVisible ? "✓ Dropdown is visible!" : "✗ Dropdown not found");
  
  // Check dropdown content
  const dropdownContent = await page.evaluate(() => {
    const dropdown = document.querySelector(".profile-dropdown");
    if (!dropdown) return null;
    
    return {
      text: dropdown.innerText,
      itemsCount: dropdown.querySelectorAll(".dropdown-item").length
    };
  });
  
  console.log("Dropdown content:", dropdownContent);
} catch (e) {
  console.error("Error:", e.message);
} finally {
  await browser.close();
}
