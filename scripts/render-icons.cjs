// Requires sharp. Rasterizes the original SVG sources for Pillow composition.
const sharp = require('sharp');
const fs = require('node:fs/promises');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
async function main() {
  const source = path.join(root, 'assets/vendor/icons');
  const target = path.join(root, '.cache/icons');
  await fs.mkdir(target, {recursive:true});
  for (const file of await fs.readdir(source)) {
    if (!file.endsWith('.svg')) continue;
    let svg = await fs.readFile(path.join(source, file), 'utf8');
    if (svg.includes('stroke="currentColor"')) svg = svg.replaceAll('stroke="currentColor"', 'stroke="#3B82F6"');
    if (file === 'modelcontextprotocol.svg') svg = svg.replace('<path ', '<path fill="#3B82F6" ');
    // Use the square logo mark from dbt's official horizontal lockup.
    if (file === 'dbt.svg') svg = svg.replace('viewBox="0 0 139 32"', 'viewBox="0 0 32 32"').replace('width="139"', 'width="32"');
    await sharp(Buffer.from(svg)).resize(56,56,{fit:'contain'}).png().toFile(path.join(target,file.replace('.svg','.png')));
  }
  console.log('Original SVG icons rendered.');
}
main().catch(error=>{console.error(error.message);process.exit(1)});
