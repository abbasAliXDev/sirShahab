const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function generateSlideImages() {
  // Create output directory if it doesn't exist
  const outputDir = path.join(__dirname, 'static/pitch_deck/images');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  try {
    const page = await browser.newPage();

    // Set viewport size for slides (1200x675 - 16:9 aspect ratio)
    await page.setViewport({
      width: 1200,
      height: 675,
      deviceScaleFactor: 2 // For higher resolution
    });

    // Process each slide
    for (let i = 1; i <= 3; i++) {
      const slideUrl = `file://${path.join(__dirname, `static/pitch_deck/slide${i}.html`)}`;
      const outputPath = path.join(outputDir, `slide${i}.png`);
      
      console.log(`Processing slide ${i}...`);
      
      await page.goto(slideUrl, {
        waitUntil: 'networkidle0',
        timeout: 60000
      });

      // Wait for fonts and other resources to load
      await page.waitForTimeout(1000);

      // Take a screenshot
      await page.screenshot({
        path: outputPath,
        fullPage: false,
        omitBackground: false
      });

      console.log(`Slide ${i} saved to ${outputPath}`);
    }
  } catch (error) {
    console.error('Error generating slides:', error);
  } finally {
    await browser.close();
    console.log('All slides generated successfully!');
  }
}

generateSlideImages();