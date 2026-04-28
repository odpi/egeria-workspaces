import fs from "node:fs";
import path from "node:path";

const vaultPath = process.argv[2];

if (!vaultPath) {
    console.error("Usage: node deploy.mjs <path-to-obsidian-vault>");
    process.exit(1);
}

const pluginId = "call-dr-egeria";
const pluginDir = path.resolve(vaultPath, ".obsidian", "plugins", pluginId);

fs.mkdirSync(pluginDir, { recursive: true });

for (const file of ["main.js", "manifest.json"]) {
    fs.copyFileSync(path.resolve(file), path.join(pluginDir, file));
    console.log(`Copied ${file} -> ${pluginDir}`);
}

if (fs.existsSync("styles.css")) {
    fs.copyFileSync(path.resolve("styles.css"), path.join(pluginDir, "styles.css"));
    console.log(`Copied styles.css -> ${pluginDir}`);
}

console.log(`Deployed ${pluginId} to ${pluginDir}`);