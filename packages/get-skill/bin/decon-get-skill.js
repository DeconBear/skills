#!/usr/bin/env node
'use strict';
/* eslint-disable no-console */
//
// @decon/get-skill — install a Claude Code skill from DeconBear/skills
// by downloading its GitHub release zip and extracting it.
//
const https = require('https');
const fs   = require('fs');
const path = require('path');
const os   = require('os');
const AdmZip = require('adm-zip');

const REPO  = 'DeconBear/skills';
const DEFAULT_VERSION = 'v0.1.0';
const KNOWN_SKILLS = ['premium-ui-gallery', 'vision', 'ocr-parser'];

function printHelp() {
  const lines = [
    'Usage: npx @decon/get-skill <skill> [--dest PATH] [--version VER]',
    '',
    'Downloads a skill from ' + REPO + ' GitHub releases and extracts it',
    'into your Claude Code skills directory.',
    '',
    'Skills:',
  ];
  for (const s of KNOWN_SKILLS) lines.push('  - ' + s);
  lines.push('');
  lines.push('Options:');
  lines.push('  --dest PATH      extract to this directory');
  lines.push('                   (default: ~/.claude/skills/<skill>)');
  lines.push('  --version VER    release version tag (default: ' + DEFAULT_VERSION + ')');
  lines.push('  --list           list known skills and exit');
  lines.push('  -h, --help       show this help');
  lines.push('');
  lines.push('Examples:');
  lines.push('  npx @decon/get-skill ocr-parser');
  lines.push('  npx @decon/get-skill vision --dest ./my-skill');
  lines.push('  npx @decon/get-skill premium-ui-gallery --version v0.2.0');
  process.stdout.write(lines.join('\n') + '\n');
}

function parseArgs(argv) {
  const out = { dest: '', version: '', list: false, help: false, skill: '' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') out.help = true;
    else if (a === '--list') out.list = true;
    else if (a === '--dest')   out.dest   = argv[++i] || '';
    else if (a === '--version')out.version= argv[++i] || '';
    else if (a.startsWith('--dest='))    out.dest    = a.slice('--dest='.length);
    else if (a.startsWith('--version=')) out.version = a.slice('--version='.length);
    else if (a.startsWith('-')) { console.error('error: unknown flag ' + a); process.exit(2); }
    else if (!out.skill) out.skill = a;
    else { console.error('error: unexpected positional argument ' + a); process.exit(2); }
  }
  return out;
}

function download(url, destFile, redirectsLeft) {
  if (redirectsLeft == null) redirectsLeft = 5;
  return new Promise((resolve, reject) => {
    if (redirectsLeft <= 0) return reject(new Error('too many redirects while fetching ' + url));
    https.get(url, (res) => {
      // Follow GitHub → objects.githubusercontent.com redirects.
      if (res.statusCode && res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        const next = new URL(res.headers.location, url).toString();
        res.resume();
        download(next, destFile, redirectsLeft - 1).then(resolve, reject);
        return;
      }
      if (res.statusCode !== 200) {
        res.resume();
        return reject(new Error('HTTP ' + res.statusCode + ' for ' + url));
      }
      const out = fs.createWriteStream(destFile);
      res.pipe(out);
      out.on('finish', () => out.close(() => resolve()));
      out.on('error', reject);
      res.on('error', reject);
    }).on('error', reject);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { printHelp(); return; }
  if (args.list)  { console.log(KNOWN_SKILLS.join('\n')); return; }

  if (!args.skill) {
    console.error('error: missing <skill> argument\n');
    printHelp();
    process.exit(2);
  }
  if (!KNOWN_SKILLS.includes(args.skill)) {
    console.error('error: unknown skill "' + args.skill + '"');
    console.error('Known skills:');
    for (const s of KNOWN_SKILLS) console.error('  - ' + s);
    process.exit(2);
  }

  const version = args.version || DEFAULT_VERSION;
  const dest    = path.resolve(
    args.dest || path.join(os.homedir(), '.claude', 'skills', args.skill)
  );
  const tag     = args.skill + '-' + version;
  const url     = 'https://github.com/' + REPO + '/releases/download/' + tag + '/' + args.skill + '.zip';

  console.log('Downloading ' + args.skill + ' ' + version + ' ...');
  console.log('  from: ' + url);
  console.log('  to:   ' + dest);

  const tmpDir  = fs.mkdtempSync(path.join(os.tmpdir(), 'decon-get-skill-'));
  const zipPath = path.join(tmpDir, args.skill + '.zip');
  try {
    await download(url, zipPath);
    console.log('  downloaded (' + fs.statSync(zipPath).size + ' bytes), extracting...');
    fs.mkdirSync(dest, { recursive: true });
    const zip = new AdmZip(zipPath);
    zip.extractAllTo(dest, /* overwrite */ true);
    console.log('\nDone. ' + args.skill + ' installed to: ' + dest);

    // Friendly next-step for skills that need an API key.
    const envExample = path.join(dest, '.env.example');
    const envFile    = path.join(dest, '.env');
    if (fs.existsSync(envExample) && !fs.existsSync(envFile)) {
      console.log('\nNext: this skill needs an API key. Copy the template and edit:');
      console.log('  cp "' + envExample + '" "' + envFile + '"');
      console.log('  # then open the .env in your editor and fill in the key(s)');
    }
  } catch (err) {
    console.error('error: ' + err.message);
    if (String(err.message).indexOf('HTTP 404') === 0) {
      console.error('  hint: ' + tag + ' not found. Check https://github.com/' + REPO + '/releases');
      console.error('        for the correct version, or omit --version to use the default.');
    }
    process.exit(1);
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  }
}

main().catch((err) => { console.error('error: ' + (err && err.message || err)); process.exit(1); });
