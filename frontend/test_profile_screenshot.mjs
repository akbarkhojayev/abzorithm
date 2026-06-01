import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();

try {
  // Set viewport size
  await page.setViewportSize({ width: 1280, height: 800 });
  
  await page.goto("http://localhost:5173", { waitUntil: "domcontentloaded" });
  await page.evaluate(() => {
    window.localStorage.setItem("Coding", "fake-token-for-testing");
  });
  await page.reload({ waitUntil: "domcontentloaded" });
  await page.waitForSelector(".userIcon", { timeout: 3000 });
  
  // Take screenshot before click
  await page.screenshot({ path: "/tmp/screenshot_before.png" });
  console.log("Before click screenshot saved");
  
  // Click the profile icon
  const userIcon = await page.$(".userIcon");
  if (userIcon) {
    await userIcon.click();
    await page.waitForTimeout(300);
    
    // Take screenshot after click
    await page.screenshot({ path: "/tmp/screenshot_after.png" });
    console.log("After click screenshot saved");
    
    // Check if modal is visible
    const isVisible = await page.evaluate(() => {
      const modal = document.querySelector(".modal");
      return modal && modal.classList.contains("active");
    });
    
    console.log("Modal visible:", isVisible);
  }
} catch (e) {
  console.error("Error:", e.message);
} finally {
  await browser.close();
}
