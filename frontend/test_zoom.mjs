import { chromium } from "playwright";

const browser = await chromium.launch({ headless: false, slowMo: 100 });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

try {
  // Navigate to app
  await page.goto("http://localhost:5173/codepanels", { waitUntil: "domcontentloaded" });
  
  // Wait for page to load
  await page.waitForTimeout(3000);

  console.log("✓ Page loaded");

  // Test zoom at different levels
  const zoomLevels = [0.8, 1.0, 1.5, 2.0];

  for (const zoom of zoomLevels) {
    console.log(`\n=== Testing at ${Math.round(zoom * 100)}% zoom ===`);
    
    await page.evaluate((z) => {
      document.body.style.zoom = z;
    }, zoom);
    
    await page.waitForTimeout(300);
    
    // Get layout info
    const layout = await page.evaluate(() => {
      const container = document.querySelector(".app-container");
      const panelLeft = document.querySelector(".panel-left");
      const panelRight = document.querySelector(".panel-right");
      const divider = document.querySelector(".divider-v");
      
      if (!panelLeft || !panelRight) return null;
      
      const containerRect = container?.getBoundingClientRect();
      const leftRect = panelLeft.getBoundingClientRect();
      const rightRect = panelRight.getBoundingClientRect();
      const dividerRect = divider?.getBoundingClientRect();
      
      return {
        containerWidth: containerRect?.width,
        leftPanel: {
          width: leftRect.width,
          left: leftRect.left,
          right: leftRect.right,
        },
        rightPanel: {
          width: rightRect.width,
          left: rightRect.left,
          right: rightRect.right,
        },
        divider: dividerRect ? {
          left: dividerRect.left,
          width: dividerRect.width,
        } : null,
        horizontalAlignment: (rightRect.left - leftRect.right),
      };
    });
    
    if (layout) {
      console.log(`Container width: ${layout.containerWidth}px`);
      console.log(`Left panel: ${layout.leftPanel.width.toFixed(2)}px`);
      console.log(`Right panel: ${layout.rightPanel.width.toFixed(2)}px`);
      console.log(`Horizontal gap: ${layout.horizontalAlignment.toFixed(2)}px`);
      
      if (Math.abs(layout.horizontalAlignment) < 5) {
        console.log("✓ Panels perfectly aligned");
      } else if (layout.horizontalAlignment > 0) {
        console.log(`⚠ Gap between panels: ${layout.horizontalAlignment.toFixed(2)}px`);
      } else {
        console.log(`✗ Overlap detected: ${Math.abs(layout.horizontalAlignment).toFixed(2)}px`);
      }
    }
    
    // Screenshot
    await page.screenshot({ path: `/tmp/zoom_${Math.round(zoom * 100)}.png` });
    console.log(`Screenshot: zoom_${Math.round(zoom * 100)}.png`);
  }

  console.log("\n=== Testing divider resize at 150% zoom ===");
  await page.evaluate(() => {
    document.body.style.zoom = 1.5;
  });

  const divider = await page.$(".divider-v");
  if (divider) {
    const box = await divider.boundingBox();
    console.log(`Divider at: ${box.x.toFixed(2)}, ${box.y.toFixed(2)}`);
    
    // Get initial widths
    const before = await page.evaluate(() => {
      const left = document.querySelector(".panel-left");
      const right = document.querySelector(".panel-right");
      return {
        leftWidth: left?.offsetWidth,
        rightWidth: right?.offsetWidth,
      };
    });
    
    console.log(`Before resize - Left: ${before.leftWidth}px, Right: ${before.rightWidth}px`);
    
    // Drag divider to the right
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.mouse.down();
    await page.mouse.move(box.x + 100, box.y + box.height / 2, { steps: 5 });
    await page.mouse.up();
    
    await page.waitForTimeout(500);
    
    const after = await page.evaluate(() => {
      const left = document.querySelector(".panel-left");
      const right = document.querySelector(".panel-right");
      return {
        leftWidth: left?.offsetWidth,
        rightWidth: right?.offsetWidth,
      };
    });
    
    console.log(`After resize - Left: ${after.leftWidth}px, Right: ${after.rightWidth}px`);
    console.log(`Left panel change: ${((after.leftWidth - before.leftWidth) / before.leftWidth * 100).toFixed(1)}%`);
    
    if (after.leftWidth > before.leftWidth) {
      console.log("✓ Divider resize works - left panel expanded");
    } else {
      console.log("✗ Divider resize failed");
    }
    
    await page.screenshot({ path: `/tmp/zoom_150_after_resize.png` });
    console.log("Screenshot: zoom_150_after_resize.png");
  }

  console.log("\n✓ All zoom tests completed successfully!");
} catch (error) {
  console.error("Test failed:", error.message);
} finally {
  await browser.close();
}
