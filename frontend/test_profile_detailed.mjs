import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();

try {
  await page.goto("http://localhost:5173", { waitUntil: "domcontentloaded" });
  await page.evaluate(() => {
    window.localStorage.setItem("Coding", "fake-token-for-testing");
  });
  await page.reload({ waitUntil: "domcontentloaded" });
  await page.waitForSelector(".userIcon", { timeout: 3000 });
  
  const userIcon = await page.$(".userIcon");
  if (userIcon) {
    await userIcon.click();
    await page.waitForTimeout(500);
    
    // Check modal visibility in detail
    const modalInfo = await page.evaluate(() => {
      const modal = document.querySelector(".modal");
      if (!modal) {
        return { exists: false };
      }
      
      const style = window.getComputedStyle(modal);
      const rect = modal.getBoundingClientRect();
      
      return {
        exists: true,
        hasActiveClass: modal.classList.contains("active"),
        opacity: style.opacity,
        display: style.display,
        visibility: style.visibility,
        transform: style.transform,
        pointerEvents: style.pointerEvents,
        position: style.position,
        top: style.top,
        right: style.right,
        zIndex: style.zIndex,
        width: rect.width,
        height: rect.height,
        x: rect.x,
        y: rect.y,
        visible: rect.width > 0 && rect.height > 0 && style.opacity > 0.5
      };
    });
    
    console.log("Modal Info:", JSON.stringify(modalInfo, null, 2));
  }
} catch (e) {
  console.error("Error:", e.message);
} finally {
  await browser.close();
}
