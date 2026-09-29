'use strict';

// Keep the full source histories in Git. Publish the same 40 snapshots the UI displays.
// Run with: node scripts/build-pages.cjs
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'dist');
const MAX_ASSET_BYTES = 25 * 1024 * 1024;
const HISTORY_LIMIT = 40;

function readJson(file) {
    return JSON.parse(fs.readFileSync(path.join(root, file), 'utf8').replace(/^\uFEFF/, ''));
}

function timestamp(value) {
    if (typeof value !== 'string') throw new Error('Missing history timestamp');
    const parts = value.trim().match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})(\.\d+)?(Z|[+-]\d{2}:?\d{2})?$/i);
    if (!parts) throw new Error(`Invalid history timestamp: ${value}`);
    const [, year, month, day, hour, minute, second, fraction = '', zone = ''] = parts;
    const calendar = new Date(Date.UTC(+year, +month - 1, +day, +hour, +minute, +second));
    if (calendar.getUTCFullYear() !== +year || calendar.getUTCMonth() !== +month - 1 ||
        calendar.getUTCDate() !== +day || +hour > 23 || +minute > 59 || +second > 59) {
        throw new Error(`Invalid history timestamp: ${value}`);
    }
    const normalizedZone = zone ? zone.toUpperCase().replace(/([+-]\d{2})(\d{2})$/, '$1:$2') : 'Z';
    const result = Date.parse(`${year}-${month}-${day}T${hour}:${minute}:${second}${fraction}${normalizedZone}`);
    if (!Number.isFinite(result)) throw new Error(`Invalid history timestamp: ${value}`);
    return result;
}

const assets = new Map();
for (const file of ['index.html', 'test.html', 'robots.txt', '_headers']) {
    assets.set(file, fs.readFileSync(path.join(root, file)));
}
for (const file of ['consensus_1d.json', 'consensus_1d_china.json', 'weekly.json']) {
    assets.set(file, Buffer.from(JSON.stringify(readJson(file))));
}
for (const file of ['history_1d.json', 'history_1d_china.json']) {
    const history = readJson(file);
    if (!Array.isArray(history)) throw new Error(`${file} must contain a history array`);
    const recent = history.map((snapshot, index) => ({ snapshot, index, time: timestamp(snapshot?.timestamp) }))
        .sort((a, b) => a.time - b.time || a.index - b.index)
        .slice(-HISTORY_LIMIT).map(({ snapshot }) => snapshot);
    assets.set(file, Buffer.from(JSON.stringify(recent)));
    console.log(`${file}: ${history.length} source snapshots -> ${recent.length} published snapshots`);
}

// Validate everything before writing; never rewrite or trim any source JSON.
for (const [file, bytes] of assets) {
    if (bytes.length > MAX_ASSET_BYTES) {
        throw new Error(`${file} is ${(bytes.length / 1024 / 1024).toFixed(2)} MiB, above the Cloudflare Pages 25 MiB limit`);
    }
}
fs.mkdirSync(output, { recursive: true });
// A fresh Pages build is expected. Refuse unrecognized files instead of silently publishing them.
const unexpected = fs.readdirSync(output).filter(file => !assets.has(file));
if (unexpected.length) throw new Error(`Unexpected files in dist: ${unexpected.join(', ')}. Use a clean build output directory.`);
for (const [file, bytes] of assets) {
    fs.writeFileSync(path.join(output, file), bytes);
    console.log(`dist/${file}: ${(bytes.length / 1024 / 1024).toFixed(2)} MiB`);
}
console.log('Build complete. Publish dist/ (not the repository root).');
