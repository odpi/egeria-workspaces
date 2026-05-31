import fs from 'fs';
import path from 'path';

const vaultPath = process.argv[2];
const isContainer = process.argv.includes('--container');

if (!vaultPath) {
    console.error('Usage: node deploy.mjs <vault-path> [--container]');
    console.error('  --container  Write containerized defaults to data.json (url: pyegeria-web)');
    process.exit(1);
}

const pluginDir = path.join(vaultPath, '.obsidian', 'plugins', 'call-dr-egeria');
if (!fs.existsSync(pluginDir)) {
    fs.mkdirSync(pluginDir, { recursive: true });
}

fs.copyFileSync('main.js', path.join(pluginDir, 'main.js'));
fs.copyFileSync('manifest.json', path.join(pluginDir, 'manifest.json'));

// Write container-appropriate defaults only on fresh install (never overwrite existing config)
if (isContainer) {
    const dataJsonPath = path.join(pluginDir, 'data.json');
    if (!fs.existsSync(dataJsonPath)) {
        const containerDefaults = {
            mcpUrl: 'http://pyegeria-web:8000/sse',
            mcpToken: 'egeria-secret-mcp-token',
            userId: 'erinoverview',
            userPass: 'secret',
            egeriaUrl: 'https://host.docker.internal:9443',
            viewServer: 'qs-view-server',
            defaultDirective: 'process',
            outboxPath: 'dr-egeria-outbox',
            inputPath: '',
            vaultRoot: '/coco-workbooks',
            verbose: true
        };
        fs.writeFileSync(dataJsonPath, JSON.stringify(containerDefaults, null, 2));
        console.log(`  Wrote container defaults to data.json (mcpUrl: pyegeria-web:8000/sse)`);
    } else {
        console.log(`  data.json already exists — skipping defaults (user config preserved)`);
    }
}

console.log(`Deployed call-dr-egeria to ${pluginDir}`);
