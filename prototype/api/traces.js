const fs = require('fs');
const path = require('path');

function findRepoRoot() {
  let p = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(p, 'docs', 'roles'))) return p;
    const parent = path.dirname(p);
    if (parent === p) break;
    p = parent;
  }
  return path.resolve(__dirname, '../..');
}

const REPO_ROOT = findRepoRoot();

function parseFrontmatter(text) {
  const m = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
  if (!m) return {};
  const fm = {};
  for (const line of m[1].split('\n')) {
    const trimmed = line.trim();
    const colonIdx = trimmed.indexOf(':');
    if (colonIdx < 0) continue;
    const key = trimmed.slice(0, colonIdx).trim();
    let val = trimmed.slice(colonIdx + 1).trim();
    if (val.startsWith('[') && val.endsWith(']')) {
      val = val
        .slice(1, -1)
        .split(',')
        .map(v => v.trim().replace(/^['"]|['"]$/g, ''))
        .filter(Boolean);
    } else if (val.startsWith('"') && val.endsWith('"')) {
      val = val.slice(1, -1);
    }
    fm[key] = val;
  }
  return fm;
}

function extractSections(text) {
  text = text.replace(/^---\s*\n[\s\S]*?\n---\s*\n/, '');
  const sections = {};
  let current = null;
  let buf = [];
  for (const line of text.split('\n')) {
    const h = line.match(/^##\s+(.+)/);
    if (h) {
      if (current) sections[current] = buf.join('\n').trim();
      current = h[1].trim();
      buf = [];
    } else if (current !== null) {
      buf.push(line);
    }
  }
  if (current) sections[current] = buf.join('\n').trim();
  return sections;
}

function cleanText(text, maxLen = 300) {
  const lines = [];
  for (let line of text.split('\n')) {
    line = line.trim();
    if (line.startsWith('- ')) line = line.slice(2);
    if (line.startsWith('### ')) line = line.slice(4);
    if (line.startsWith('**') && line.endsWith('**')) line = line.slice(2, -2);
    if (line) lines.push(line);
  }
  const result = lines.join(' ');
  return result.length > maxLen ? result.slice(0, maxLen) + '...' : result;
}

function getSection(sections, ...names) {
  for (const name of names) if (sections[name]) return sections[name];
  return '';
}

function parseTrace(filepath) {
  let text;
  try {
    text = fs.readFileSync(filepath, 'utf-8');
  } catch {
    return null;
  }
  const fm = parseFrontmatter(text);
  if (!fm.date) return null;
  const sections = extractSections(text);
  const stat = fs.statSync(filepath);
  return {
    filepath: path.relative(REPO_ROOT, filepath).replace(/\\/g, '/'),
    date: fm.date,
    mtime: stat.mtimeMs,
    type: fm.type || 'trace',
    role: fm.role || '',
    topic: fm.topic || path.basename(filepath, '.md'),
    tags: fm.tags || [],
    summary: cleanText(
      getSection(sections, '핵심 내용', '핵심 내용 / Key Content', '목적', '목적 / Purpose')
    ),
    decision: cleanText(
      getSection(sections, '결정사항', '결정사항 / Decision', '결정'),
      200
    ),
    insight: cleanText(
      getSection(sections, '인사이트', '인사이트 / Insights', '이 세션에서 알게 된 것', '알게 된 것'),
      200
    ),
    open_thinking: fm.open_thinking || [],
  };
}

function loadAll() {
  const traces = [];
  const docs = path.join(REPO_ROOT, 'docs');
  const rolesDir = path.join(docs, 'roles');
  if (fs.existsSync(rolesDir)) {
    for (const role of fs.readdirSync(rolesDir)) {
      const roleDir = path.join(rolesDir, role);
      if (!fs.statSync(roleDir).isDirectory()) continue;
      const tracesDir = path.join(roleDir, 'traces');
      if (!fs.existsSync(tracesDir)) continue;
      for (const f of fs.readdirSync(tracesDir).sort()) {
        if (!f.endsWith('.md')) continue;
        const t = parseTrace(path.join(tracesDir, f));
        if (t) traces.push(t);
      }
    }
  }
  const meetingsDir = path.join(docs, 'shared', 'meetings');
  if (fs.existsSync(meetingsDir)) {
    for (const m of fs.readdirSync(meetingsDir).sort()) {
      const mDir = path.join(meetingsDir, m);
      if (!fs.statSync(mDir).isDirectory()) continue;
      const summary = path.join(mDir, 'summary.md');
      if (fs.existsSync(summary)) {
        const t = parseTrace(summary);
        if (t) {
          t.type = 'meeting';
          traces.push(t);
        }
      }
    }
  }
  traces.sort((a, b) => {
    if (a.date !== b.date) return b.date.localeCompare(a.date);
    return b.mtime - a.mtime;
  });
  return traces;
}

async function handler(req, res) {
  try {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json');
    if (req.method === 'OPTIONS') {
      res.statusCode = 200;
      res.end();
      return;
    }
    const url = new URL(req.url, 'http://localhost');
    const role = url.searchParams.get('role') || 'all';
    const days = parseInt(url.searchParams.get('days') || '30', 10);

    const all = loadAll();
    // Day-granular cutoff to avoid timezone/hour boundary issues
    const cutoffDate = days >= 9999
      ? null
      : new Date(Date.now() - days * 86400000).toISOString().slice(0, 10);
    const filtered = all.filter(t => {
      if (role !== 'all' && t.role !== role && t.type !== 'meeting') return false;
      if (cutoffDate && t.date < cutoffDate) return false;
      return true;
    });

    res.statusCode = 200;
    res.end(JSON.stringify({ traces: filtered, count: filtered.length, repo_root: REPO_ROOT }));
  } catch (e) {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: e.message, stack: e.stack }));
  }
}

module.exports = handler;
module.exports.config = { maxDuration: 10 };
module.exports.loadAll = loadAll;
module.exports.parseTrace = parseTrace;
module.exports.REPO_ROOT = REPO_ROOT;
