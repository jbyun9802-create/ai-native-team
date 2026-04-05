#!/usr/bin/env python3
"""
TeamBrain TUI — 팀 멘탈 모델 터미널 대시보드

Usage:
    python prototype/brain-tui.py
    python prototype/brain-tui.py --repo /path/to/repo
"""

import os
import re
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Static, Label, Rule
from textual.reactive import reactive
from rich.text import Text

# ═══════════════════════════════════════
# CONFIG — 역할 스타일만 고정, 데이터는 파일에서
# ═══════════════════════════════════════

ROLE_STYLES = {
    "pm":          {"label": "PM",          "color": "bright_blue"},
    "engineering": {"label": "Engineering", "color": "bright_green"},
    "design":      {"label": "Design",      "color": "bright_yellow"},
    "uxr":         {"label": "UX Research", "color": "bright_red"},
    "gtm":         {"label": "GTM",         "color": "bright_cyan"},
}

PERIOD_OPTIONS = [(1, "1일"), (7, "7일"), (30, "30일"), (9999, "전체")]

# ═══════════════════════════════════════
# REPO DETECTION
# ═══════════════════════════════════════

def find_repo_root():
    for i, arg in enumerate(sys.argv):
        if arg == "--repo" and i + 1 < len(sys.argv):
            return Path(sys.argv[i + 1])
    p = Path.cwd()
    for _ in range(10):
        if (p / "docs" / "roles").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    p = Path(__file__).resolve().parent
    for _ in range(10):
        if (p / "docs" / "roles").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    return Path.cwd()

# ═══════════════════════════════════════
# PARSING — brain.py와 동일 로직
# ═══════════════════════════════════════

def parse_frontmatter(text):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        line = line.strip()
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key, val = key.strip(), val.strip()
        if val.startswith('[') and val.endswith(']'):
            val = [v.strip().strip("'\"") for v in val[1:-1].split(',') if v.strip()]
        elif val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        fm[key] = val
    return fm


def extract_sections(text):
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)
    sections = {}
    current = None
    lines = []
    for line in text.split('\n'):
        heading = re.match(r'^##\s+(.+)', line)
        if heading:
            if current:
                sections[current] = '\n'.join(lines).strip()
            current = heading.group(1).strip()
            lines = []
        elif current is not None:
            lines.append(line)
    if current:
        sections[current] = '\n'.join(lines).strip()
    return sections


def clean_text(text, max_len=300):
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('- '):
            line = line[2:]
        if line.startswith('### '):
            line = line[4:]
        if line.startswith('**') and line.endswith('**'):
            line = line[2:-2]
        if line:
            lines.append(line)
    result = ' '.join(lines)
    return result[:max_len] + '...' if len(result) > max_len else result


def get_section(sections, *names):
    for name in names:
        if name in sections:
            return sections[name]
    return ""


def parse_trace(filepath):
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return None
    fm = parse_frontmatter(text)
    if not fm.get("date"):
        return None
    sections = extract_sections(text)
    mtime = filepath.stat().st_mtime
    return {
        "filepath": str(filepath),
        "date": fm.get("date", ""),
        "mtime": mtime,
        "type": fm.get("type", "trace"),
        "role": fm.get("role", ""),
        "topic": fm.get("topic", filepath.stem),
        "tags": fm.get("tags", []),
        "summary": clean_text(get_section(sections,
            "핵심 내용", "핵심 내용 / Key Content", "목적", "목적 / Purpose")),
        "decision": clean_text(get_section(sections,
            "결정사항", "결정사항 / Decision", "결정"), 200),
        "insight": clean_text(get_section(sections,
            "인사이트", "인사이트 / Insights", "이 세션에서 알게 된 것", "알게 된 것"), 200),
    }


def load_all(repo_root):
    traces = []
    docs = repo_root / "docs"
    roles_dir = docs / "roles"
    if roles_dir.exists():
        for role_dir in roles_dir.iterdir():
            if not role_dir.is_dir():
                continue
            traces_dir = role_dir / "traces"
            if not traces_dir.exists():
                continue
            for f in sorted(traces_dir.glob("*.md")):
                t = parse_trace(f)
                if t:
                    traces.append(t)
    meetings_dir = docs / "shared" / "meetings"
    if meetings_dir.exists():
        for mdir in sorted(meetings_dir.iterdir()):
            if not mdir.is_dir():
                continue
            summary = mdir / "summary.md"
            if summary.exists():
                t = parse_trace(summary)
                if t:
                    t["type"] = "meeting"
                    traces.append(t)
    traces.sort(key=lambda t: (t["date"], t.get("mtime", 0)), reverse=True)
    return traces


def discover_roles(traces):
    roles = {}
    for t in traces:
        role = t["role"]
        if role and role != "all" and role not in roles:
            style = ROLE_STYLES.get(role, {"label": role, "color": "white"})
            roles[role] = {
                "role": role, "label": style["label"], "color": style["color"],
                "trace_count": 0, "last_date": "",
            }
        if role in roles:
            roles[role]["trace_count"] += 1
            if t["date"] > roles[role]["last_date"]:
                roles[role]["last_date"] = t["date"]
    return roles


def get_role_traces(all_traces, role):
    own = [t for t in all_traces if t["role"] == role]
    meetings = [t for t in all_traces if t["type"] == "meeting"]
    seen = set()
    result = []
    for t in own + meetings:
        if t["filepath"] not in seen:
            seen.add(t["filepath"])
            result.append(t)
    result.sort(key=lambda t: (t["date"], t.get("mtime", 0)), reverse=True)
    return result


# ═══════════════════════════════════════
# TEXTUAL WIDGETS
# ═══════════════════════════════════════

class RoleButton(Static):
    def __init__(self, role, label, color, **kwargs):
        super().__init__(**kwargs)
        self.role_id = role
        self.role_label = label
        self.role_color = color

    def on_click(self):
        self.app.select_role(self.role_id)

    def render(self):
        selected = self.app.selected_role == self.role_id
        marker = "●" if selected else "○"
        style = f"bold {self.role_color}" if selected else "dim"
        text = Text()
        text.append(f" {marker} ", style=self.role_color)
        text.append(f"{self.role_label}", style=style)
        return text


class PeriodButton(Static):
    def __init__(self, days, label, **kwargs):
        super().__init__(**kwargs)
        self.days = days
        self.period_label = label

    def on_click(self):
        self.app.select_period(self.days)

    def render(self):
        selected = self.app.selected_period == self.days
        if selected:
            return Text(f" [{self.period_label}] ", style="bold bright_blue on grey15")
        return Text(f"  {self.period_label}  ", style="dim")


class TraceItem(Static):
    def __init__(self, trace, color, is_first=False, **kwargs):
        super().__init__(**kwargs)
        self.trace = trace
        self.trace_color = color
        self.is_first = is_first

    def on_click(self):
        filepath = self.trace.get("filepath", "")
        if filepath and os.path.exists(filepath):
            try:
                subprocess.Popen(["code", filepath], shell=True,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                try:
                    os.startfile(filepath)
                except Exception:
                    pass

    def render(self):
        t = self.trace
        text = Text()
        marker = "┃" if self.is_first else "│"
        text.append(f" {marker} ", style=self.trace_color)

        if t["type"] == "meeting":
            text.append("◆ MEETING ", style="bright_magenta")
        else:
            text.append("● TRACE ", style=self.trace_color)
        text.append(f"{t['date']}\n", style="dim")

        text.append(f" {marker} ", style=self.trace_color if self.is_first else "dim")
        text.append(f"{t['topic']}\n", style="bold")

        if t.get("insight"):
            display = t["insight"][:150] + "..." if len(t["insight"]) > 150 else t["insight"]
            text.append(f" {marker} ", style="dim")
            text.append(f'"{display}"\n', style="italic grey70")

        if t.get("decision"):
            display = t["decision"][:120] + "..." if len(t["decision"]) > 120 else t["decision"]
            text.append(f" {marker} ", style="dim")
            text.append(f"-> {display}\n", style="grey50")

        text.append(f" {marker} ", style="dim")
        text.append("click to open file", style="dim italic")
        return text


# ═══════════════════════════════════════
# APP
# ═══════════════════════════════════════

class BrainApp(App):
    CSS = """
    Screen { background: #08080d; }
    #sidebar { width: 26; background: #0e0e16; border-right: solid #1c1c2a; padding: 1 0; }
    #sidebar-title { text-align: center; color: #6366f1; text-style: bold; padding: 0 1 1 1; }
    RoleButton { height: 2; padding: 0 1; }
    RoleButton:hover { background: #14141e; }
    #main-panel { padding: 0 1; }
    #period-bar { height: 3; padding: 1 0 0 0; layout: horizontal; }
    PeriodButton { width: auto; min-width: 8; height: 1; }
    PeriodButton:hover { background: #14141e; }
    #mind-section { height: auto; background: #0e0e16; border: solid #1c1c2a; margin: 1 0; padding: 0; }
    #content-scroll { height: 1fr; }
    #timeline-header { padding: 1 0 0 1; color: #8888a0; }
    TraceItem { height: auto; padding: 0 1; margin: 0 0 1 0; background: #0e0e16; border: solid #1c1c2a; }
    TraceItem:hover { background: #14141e; border: solid #2a2a3e; }
    Rule { color: #1c1c2a; margin: 0; }
    #search-display { width: auto; min-width: 20; height: 1; margin: 0 0 0 2; color: #f59e0b; }
    #search-input { margin: 0 0 1 0; background: #14141e; border: solid #6366f1; color: #e0e0e8; }
    """

    BINDINGS = [
        Binding("1", "period_1", "1일"),
        Binding("2", "period_7", "7일"),
        Binding("3", "period_30", "30일"),
        Binding("4", "period_all", "전체"),
        Binding("tab", "next_role", "다음"),
        Binding("shift+tab", "prev_role", "이전"),
        Binding("/", "search", "검색"),
        Binding("escape", "clear_search", "초기화"),
        Binding("5", "drill_1", "고민1"),
        Binding("6", "drill_2", "고민2"),
        Binding("7", "drill_3", "고민3"),
        Binding("8", "drill_4", "고민4"),
        Binding("9", "drill_5", "고민5"),
        Binding("r", "reload", "새로고침"),
        Binding("q", "quit", "종료"),
    ]

    selected_role = reactive("", init=False)
    selected_period = reactive(30, init=False)
    search_query = reactive("", init=False)

    def __init__(self, repo_root):
        super().__init__()
        self.repo_root = repo_root
        self.all_traces = load_all(repo_root)
        self.roles = discover_roles(self.all_traces)
        self.role_order = sorted(self.roles.keys(), key=lambda r: self.roles[r]["last_date"], reverse=True)
        self._initial_role = self.role_order[0] if self.role_order else ""
        self.title = "TeamBrain"
        self.sub_title = "Team Mental Model"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label(" TEAMBRAIN", id="sidebar-title")
                yield Rule()
                for role in self.role_order:
                    info = self.roles[role]
                    yield RoleButton(role, info["label"], info["color"])
            with Vertical(id="main-panel"):
                with Horizontal(id="period-bar"):
                    for days, label in PERIOD_OPTIONS:
                        yield PeriodButton(days, label)
                    yield Static("", id="search-display")
                with ScrollableContainer(id="content-scroll"):
                    yield Static(id="mind-section")
                    yield Label("  사고 흐름", id="timeline-header")
        yield Footer()

    def on_mount(self):
        self.selected_role = self._initial_role
        self.refresh_view()

    def watch_selected_role(self, value):
        self.refresh_view()

    def watch_selected_period(self, value):
        self.refresh_view()

    def watch_search_query(self, value):
        try:
            sd = self.query_one("#search-display", Static)
            sd.update(f"🔍 \"{value}\"" if value else "")
        except Exception:
            pass
        self.refresh_view()

    def select_role(self, role):
        self.selected_role = role

    def select_period(self, days):
        self.selected_period = days

    def get_filtered(self):
        role = self.selected_role
        days = self.selected_period
        query = self.search_query.lower().strip()

        if query:
            # Search across ALL roles
            traces = list(self.all_traces)
        else:
            traces = get_role_traces(self.all_traces, role)

        if days < 9999:
            all_dates = [t["date"] for t in self.all_traces if t["date"]]
            ref_date = max(all_dates) if all_dates else datetime.now().strftime("%Y-%m-%d")
            ref = datetime.strptime(ref_date, "%Y-%m-%d")
            cutoff = (ref - timedelta(days=days)).strftime("%Y-%m-%d")
            traces = [t for t in traces if t["date"] >= cutoff]

        if query:
            traces = self._semantic_search(traces, query)

        return traces

    def _semantic_search(self, traces, query):
        """Use Claude API to find traces semantically related to query."""
        # Build trace summaries for Claude
        trace_list = []
        for i, t in enumerate(traces):
            tags = ", ".join(t["tags"]) if isinstance(t.get("tags"), list) else str(t.get("tags", ""))
            trace_list.append(
                f"[{i}] {t['date']} | {t.get('role','')} | {t['topic']} | "
                f"insight: {t.get('insight','')[:150]} | decision: {t.get('decision','')[:100]} | "
                f"summary: {t.get('summary','')[:100]} | tags: {tags}"
            )

        if not trace_list:
            return []

        prompt = (
            f"아래는 팀의 작업 기록(traces) 목록이다.\n"
            f"사용자가 \"{query}\"를 검색했다.\n"
            f"이 검색어와 의미적으로 관련된 trace를 찾아서 각각 관련 부분을 1줄 excerpt로 뽑아줘.\n"
            f"직접 단어가 포함되지 않아도 주제/맥락이 관련되면 포함.\n"
            f"관련 없으면 빈 배열.\n\n"
            + "\n".join(trace_list)
            + '\n\nJSON 배열만 반환 (설명 없이): [{"id": 번호, "excerpt": "관련 ��분 1줄 요약"}, ...]'
        )

        try:
            from anthropic import Anthropic
            # Load API key from .env
            env_path = self.repo_root / "prototype" / ".env"
            api_key = None
            if env_path.exists():
                for line in env_path.read_text(encoding="utf-8").split("\n"):
                    if line.startswith("ANTHROPIC_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
            if not api_key:
                api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                # Fallback to simple text match
                return [t for t in traces if query in (t.get("topic","") + t.get("insight","") + t.get("summary","")).lower()]

            client = Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )

            result_text = response.content[0].text.strip()
            match = re.search(r'\[.*\]', result_text, re.DOTALL)
            if match:
                results = json.loads(match.group())
                out = []
                for r in results:
                    idx = r.get("id", -1) if isinstance(r, dict) else r
                    if 0 <= idx < len(traces):
                        t = dict(traces[idx])
                        if isinstance(r, dict) and r.get("excerpt"):
                            t["_excerpt"] = r["excerpt"]
                        out.append(t)
                return out
            return []

        except Exception:
            return self._text_search(traces, query)

    def _text_search(self, traces, query):
        """Fallback: simple text match."""
        return [t for t in traces if query in (t.get("topic","") + t.get("insight","") + t.get("summary","")).lower()]

    def _get_api_client(self):
        """Get Anthropic client, or None."""
        try:
            from anthropic import Anthropic
            env_path = self.repo_root / "prototype" / ".env"
            api_key = None
            if env_path.exists():
                for line in env_path.read_text(encoding="utf-8").split("\n"):
                    if line.startswith("ANTHROPIC_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
            if not api_key:
                api_key = os.environ.get("ANTHROPIC_API_KEY")
            return Anthropic(api_key=api_key) if api_key else None
        except Exception:
            return None

    # ── Brain Map: 사고 에너지 분석 ──

    _brain_cache = {}  # (role, period) -> brain map result

    def _analyze_brain(self, traces, role, period):
        """Claude가 traces를 읽고 사고 에너지 분배를 분석."""
        cache_key = (role, period)
        if cache_key in self._brain_cache:
            return self._brain_cache[cache_key]

        mind_traces = [t for t in traces if t["type"] != "meeting"]
        if not mind_traces:
            return []

        trace_texts = []
        for t in mind_traces:
            trace_texts.append(
                f"- {t['date']} | {t['topic']} | "
                f"insight: {t.get('insight','')[:200]} | "
                f"decision: {t.get('decision','')[:150]}"
            )

        prompt = (
            f"아래는 한 팀원({role})의 최근 작업 기록(traces)이다.\n\n"
            + "\n".join(trace_texts)
            + "\n\n이 사람의 머릿속을 분석해줘. "
            f"이 사람이 가장 많이 고민하고 있는 주제를 3~5개 뽑아줘.\n"
            f"각 주제는:\n"
            f"- label: 한 줄 요약 (이 사람이 고민하는 질문 형태)\n"
            f"- detail: 구체적으로 뭘 했는지 한 줄\n"
            f"- weight: 사고 에너지 비중 (전체 합 100)\n\n"
            f'JSON 배열만: [{{"label":"...", "detail":"...", "weight": N}}, ...]'
        )

        client = self._get_api_client()
        if not client:
            return self._fallback_brain(mind_traces)

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                result = json.loads(match.group())
                self._brain_cache[cache_key] = result
                return result
        except Exception:
            pass
        return self._fallback_brain(mind_traces)

    def _fallback_brain(self, traces):
        """API 없을 때 — 그냥 최근 traces의 topic을 보여줌."""
        seen = []
        for t in traces[:5]:
            seen.append({"label": t["topic"], "detail": "", "weight": 100 // max(len(traces[:5]), 1)})
        return seen

    def _analyze_thought_evolution(self, traces, theme_label):
        """선택된 고민 주제의 시간에 따른 변화를 분석."""
        mind_traces = [t for t in traces if t["type"] != "meeting"]
        if not mind_traces:
            return None

        trace_texts = []
        for t in mind_traces:
            trace_texts.append(
                f"- {t['date']} | {t['topic']} | "
                f"insight: {t.get('insight','')[:200]} | "
                f"decision: {t.get('decision','')[:150]}"
            )

        prompt = (
            f"아래는 한 팀원의 작업 기록이다.\n\n"
            + "\n".join(trace_texts)
            + f"\n\n이 사람의 고민 중 \"{theme_label}\"에 대해 분석해줘.\n"
            f"시간 순서대로 이 고민이 어떻게 변화했는지 보여줘.\n"
            f"각 단계:\n"
            f"- date: 날짜\n"
            f"- thought: 그 시점의 핵심 생각 (인용 또는 요약)\n\n"
            f"마지막에 flow: 한 줄로 전체 흐름 요약\n\n"
            f'JSON: {{"steps": [{{"date":"...", "thought":"..."}}, ...], "flow": "..."}}'
        )

        client = self._get_api_client()
        if not client:
            return None

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass
        return None

    def refresh_view(self):
        role = self.selected_role
        query = self.search_query.lower().strip()

        if not role and not query:
            return
        if role and role not in self.roles and not query:
            return

        # When searching, use default color; otherwise role color
        if query:
            color = "bright_yellow"
        elif role in self.roles:
            color = self.roles[role]["color"]
        else:
            color = "white"

        events = self.get_filtered()

        period_label = "전체" if self.selected_period >= 9999 else f"{self.selected_period}일"
        mind_text = Text()

        if query:
            # Search mode — show search results
            mind_traces = sorted([t for t in events if t["type"] != "meeting"],
                                 key=lambda t: (t["date"], t.get("mtime", 0)), reverse=True)
            mind_text.append(f"  검색 결과: \"{query}\" ", style="bold bright_yellow")
            mind_text.append(f"({len(mind_traces)}건)\n", style="dim")
            mind_text.append("  -" * 20 + "\n", style="grey23")
            if not mind_traces:
                mind_text.append("\n  매칭되는 trace 없음\n", style="dim italic")
            else:
                for i, t in enumerate(mind_traces[:8]):
                    ms = color if i == 0 else "grey30"
                    mind_text.append(f"\n  | ", style=ms)
                    mind_text.append(f"[{t['role']}] {t['topic']}\n", style="bold" if i == 0 else "")
                    excerpt = t.get("_excerpt", "")
                    if excerpt:
                        mind_text.append(f"  | ", style="bright_yellow")
                        mind_text.append(f"{excerpt}\n", style="italic bright_yellow")
                    mind_text.append(f"  | ", style="grey23")
                    mind_text.append(f"{t['date']}\n", style="dim")
        else:
            # Brain map mode — 사고 에너지 분석
            mind_text.append(f"  지금 머릿속 ", style="bold")
            mind_text.append(f"(최근 {period_label})\n", style="dim")
            mind_text.append("  -" * 20 + "\n", style="grey23")

            brain = self._analyze_brain(events, role, self.selected_period)
            if not brain:
                mind_text.append("\n  이 기간에 기록된 trace 없음\n", style="dim italic")
            else:
                self._current_brain = brain  # store for drill-down
                for i, item in enumerate(brain):
                    w = item.get("weight", 0)
                    bar_len = max(1, int(w / 100 * 30))
                    bar = "█" * bar_len

                    mind_text.append(f"\n  ", style="")
                    mind_text.append(f"[{i+1}] ", style="bold " + color if i == 0 else "bold grey50")
                    mind_text.append(f"{item['label']}\n", style="bold" if i == 0 else "")
                    mind_text.append(f"      ", style="")
                    mind_text.append(f"{bar} {w}%\n", style=color if i == 0 else "grey42")
                    if item.get("detail"):
                        mind_text.append(f"      ", style="")
                        mind_text.append(f"{item['detail']}\n", style="dim")

                mind_text.append(f"\n  숫자 키(5-9)로 고민 선택 → 변화 보기\n", style="dim italic")

        self.query_one("#mind-section", Static).update(mind_text)

        # Period & role buttons
        for btn in self.query(PeriodButton):
            btn.refresh()
        for btn in self.query(RoleButton):
            btn.refresh()

        # Timeline — mount into content-scroll, after mind-section and header
        container = self.query_one("#content-scroll", ScrollableContainer)
        # Remove only TraceItem and date-sep labels (keep mind-section and timeline-header)
        for child in list(container.children):
            if isinstance(child, (TraceItem, Label)) and child.id not in ("mind-section", "timeline-header"):
                if isinstance(child, TraceItem) or (isinstance(child, Label) and child.id is None):
                    child.remove()

        if query:
            timeline_traces = sorted(events, key=lambda t: (t["date"], t.get("mtime", 0)), reverse=True)
        else:
            timeline_traces = get_role_traces(self.all_traces, role)
            timeline_traces.sort(key=lambda t: (t["date"], t.get("mtime", 0)), reverse=True)

        cur_date = ""
        for i, t in enumerate(timeline_traces):
            if t["date"] != cur_date:
                cur_date = t["date"]
                container.mount(Label(f"  -- {t['date']} {'--' * 20}"))
            container.mount(TraceItem(t, color, is_first=(i == 0)))

    def action_search(self):
        """Open search input dialog."""
        from textual.widgets import Input
        # If already searching, do nothing
        try:
            self.query_one("#search-input", Input)
            return
        except Exception:
            pass
        inp = Input(placeholder="검색어 입력 (topic, insight, decision, tags)", id="search-input")
        self.query_one("#main-panel", Vertical).mount(inp, before=self.query_one("#mind-section"))
        inp.focus()

    def on_input_submitted(self, event):
        """Handle search input submission."""
        self.search_query = event.value
        try:
            event.input.remove()
        except Exception:
            pass

    def action_clear_search(self):
        """Clear search, reset drill-down, refresh view."""
        self.search_query = ""
        try:
            from textual.widgets import Input
            self.query_one("#search-input", Input).remove()
        except Exception:
            pass
        self.refresh_view()

    def action_period_1(self):
        self.selected_period = 1
    def action_period_7(self):
        self.selected_period = 7
    def action_period_30(self):
        self.selected_period = 30
    def action_period_all(self):
        self.selected_period = 9999

    # ── Drill down into a brain theme ──
    _current_brain = []

    def _drill_into(self, index):
        if not self._current_brain or index >= len(self._current_brain):
            return
        theme = self._current_brain[index]
        events = self.get_filtered()
        role = self.selected_role
        color = self.roles[role]["color"] if role in self.roles else "white"

        result = self._analyze_thought_evolution(events, theme["label"])
        mind_text = Text()
        mind_text.append(f"  {theme['label']}\n", style="bold " + color)
        mind_text.append("  -" * 20 + "\n", style="grey23")

        if result and result.get("steps"):
            for step in result["steps"]:
                mind_text.append(f"\n  {step['date']}  ", style="bold grey70")
                mind_text.append(f"{step['thought']}\n", style="")
            if result.get("flow"):
                mind_text.append(f"\n  흐름: ", style="bold grey50")
                mind_text.append(f"{result['flow']}\n", style="italic grey62")
        else:
            mind_text.append("\n  분석 데이터 부족\n", style="dim italic")

        mind_text.append(f"\n  Escape로 돌아가기\n", style="dim italic")
        self.query_one("#mind-section", Static).update(mind_text)

    def action_drill_1(self): self._drill_into(0)
    def action_drill_2(self): self._drill_into(1)
    def action_drill_3(self): self._drill_into(2)
    def action_drill_4(self): self._drill_into(3)
    def action_drill_5(self): self._drill_into(4)

    def action_reload(self):
        """파일 시스템에서 traces를 다시 읽어 화면 갱신."""
        self.all_traces = load_all(self.repo_root)
        self.roles = discover_roles(self.all_traces)
        self.role_order = sorted(self.roles.keys(), key=lambda r: self.roles[r]["last_date"], reverse=True)
        self._brain_cache.clear()
        self.refresh_view()
        self.notify("새로고침 완료")

    def action_next_role(self):
        if not self.role_order:
            return
        idx = self.role_order.index(self.selected_role) if self.selected_role in self.role_order else -1
        self.selected_role = self.role_order[(idx + 1) % len(self.role_order)]
    def action_prev_role(self):
        if not self.role_order:
            return
        idx = self.role_order.index(self.selected_role) if self.selected_role in self.role_order else 0
        self.selected_role = self.role_order[(idx - 1) % len(self.role_order)]


# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════

if __name__ == "__main__":
    repo = find_repo_root()
    if not (repo / "docs").exists():
        print(f"Error: docs/ not found in {repo}")
        print("Usage: python brain-tui.py --repo /path/to/project")
        sys.exit(1)
    app = BrainApp(repo)
    app.run()
