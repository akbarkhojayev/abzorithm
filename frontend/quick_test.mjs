import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();

try {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("http://localhost:5173", { waitUntil: "domcontentloaded" });
  await page.evaluate(() => {
    window.localStorage.setItem("Coding", "test-token");
  });
  await page.reload({ waitUntil: "domcontentloaded" });
  
  await page.waitForSelector(".userIcon", { timeout: 5000 });
  await page.waitForTimeout(200);
  
  // Click profile button
  await page.click(".userIcon");
  await page.waitForTimeout(300);
  
  // Check dropdown visibility and position
  const result = await page.evaluate(() => {
    const navbar = document.querySelector(".navbar");
    const dropdown = document.querySelector(".profile-dropdown");
    
    if (!dropdown) return { dropdown: false };
    
    const navbarRect = navbar.getBoundingClientRect();
    const dropdownRect = dropdown.getBoundingClientRect();
    
    return {
      dropdown: true,
      navbarTop: navbarRect.top,
      navbarBottom: navbarRect.bottom,
      dropdownTop: dropdownRect.top,
      dropdownBottom: dropdownRect.bottom,
      isAboveNavbar: dropdownRect.bottom > navbarRect.bottom,
      dropdownVisible: dropdownRect.width > 0 && dropdownRect.height > 0
    };
  });
  
  console.log("Result:", result);
  
  if (result.dropdown && result.isAboveNavbar && result.dropdownVisible) {
    console.log("✓ SUCCESS! Dropdown appears above navbar");
  } else if (!result.dropdown) {
    console.log("✗ Dropdown not found in DOM");
  } else {
    console.log("✗ Dropdown positioning issue");
  }
  
} catch (e) {
  console.error("✗ Error:", e.message);
} finally {
  await browser.close();
}
