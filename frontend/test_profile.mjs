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
  
  await page.waitForSelector(".userIcon", { timeout: 5000 });
  await page.waitForTimeout(500);
  
  await page.screenshot({ path: "/tmp/new_before.png" });
  console.log("✓ Screenshot before click");
  
  await page.$eval(".userIcon", el => el.click());
  await page.waitForTimeout(500);
  
  await page.screenshot({ path: "/tmp/new_after.png" });
  console.log("✓ Screenshot after click");
  
  const dropdown = await page.evaluate(() => {
    const d = document.querySelector(".profile-dropdown");
    return d !== null;
  });
  
  console.log(dropdown ? "✓ Dropdown appears!" : "✗ No dropdown");
  
} catch (e) {
  console.error("Error:", e.message);
} finally {
  await browser.close();
}
