const fs = require('fs');
const path = require('path');
const tracesMod = require('./traces');

const REPO_ROOT = tracesMod.REPO_ROOT;

const ROLE_TO_FRAMEWORK = {
  pm: 'pm-thinking',
  engineering: 'engineering-thinking',
  design: 'design-thinking',
  uxr: 'uxr-thinking',
  gtm: 'growth-thinking',
};

function readFile(relPath) {
  try {
    return fs.readFileSync(path.join(REPO_ROOT, relPath), 'utf-8');
  } catch {
    return '';
  }
}

function loadAllFrameworks() {
  const out = {};
  for (const [role, name] of Object.entries(ROLE_TO_FRAMEWORK)) {
    const content = readFile(`docs/shared/product/specs/frameworks/${name}.md`);
    out[role] = { name, content };
  }
  return out;
}

function recentTracesDigest(limit = 10) {
  const all = tracesMod.loadAll();
  return all.slice(0, limit).map(t => ({
    date: t.date,
    role: t.role,
    type: t.type,
    topic: t.topic,
    summary: t.summary ? t.summary.slice(0, 200) : '',
  }));
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
    const role = url.searchParams.get('role') || 'pm';

    const skill = readFile('.claude/skills/save/SKILL.md');
    const allFrameworks = loadAllFrameworks();
    const currentFw = allFrameworks[role] || allFrameworks.pm;

    res.statusCode = 200;
    res.end(
      JSON.stringify({
        skill,
        current_role: role,
        current_framework: currentFw.content,
        current_framework_name: currentFw.name,
        all_frameworks: allFrameworks,
        recent_traces: recentTracesDigest(10),
      })
    );
  } catch (e) {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: e.message, stack: e.stack }));
  }
}

module.exports = handler;
module.exports.config = { maxDuration: 10 };
