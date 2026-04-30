import fs from 'fs';
import path from 'path';

const vaultPath = process.argv[2];
if (!vaultPath) {
    console.error('Please provide a vault path');
    process.exit(1);
}

const pluginDir = path.join(vaultPath, '.obsidian', 'plugins', 'calling-the-dr');
if (!fs.existsSync(pluginDir)) {
    fs.mkdirSync(pluginDir, { recursive: true });
}

fs.copyFileSync('main.js', path.join(pluginDir, 'main.js'));
fs.copyFileSync('manifest.json', path.join(pluginDir, 'manifest.json'));

console.log(`Deployed calling-the-dr to ${pluginDir}`);
