"""Build the deployable static catalogue using only Python's standard library."""
from pathlib import Path
from datetime import date, timedelta
import html
import json
import shutil
from studyflow import latest_materials, sprint_capacity, capacity_summary

ROOT = Path(__file__).parent


def build():
    materials = json.loads((ROOT/'materials.json').read_text(encoding='utf-8'))
    backlog = json.loads((ROOT/'backlog.json').read_text(encoding='utf-8'))
    vacation = [date(2026, 11, 23)+timedelta(days=i) for i in range(5)]
    available = sprint_capacity(date(2026, 11, 16), date(2026, 12, 2), 1, vacation)
    summary = capacity_summary(backlog, available)
    cards = ''.join(f'<article data-topic="{html.escape(m["topic"])}"><small>{html.escape(m["topic"])} · {m["minutes"]} мин</small><h3>{html.escape(m["title"])}</h3><p>{html.escape(m["summary"])}</p><button data-id="{m["id"]}">Изучить материал</button></article>' for m in latest_materials(materials))
    template = (ROOT/'template.html').read_text(encoding='utf-8')
    page = template.replace('{{CARDS}}', cards).replace('{{COUNT}}', str(len(materials)))
    page = page.replace('{{PLANNED}}', str(summary['planned'])).replace('{{CAPACITY}}', str(available)).replace('{{OVERLOAD}}', str(summary['overload']))
    out = ROOT/'dist'
    out.mkdir(exist_ok=True)
    (out/'index.html').write_text(page, encoding='utf-8')
    (out/'capacity.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    shutil.copy2(ROOT/'materials.json', out/'materials.json')
    print(f'Built {len(materials)} materials; capacity={available}, planned={summary["planned"]}, overload={summary["overload"]}')
    return out


if __name__ == '__main__':
    build()
