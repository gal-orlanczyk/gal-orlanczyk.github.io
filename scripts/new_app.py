#!/usr/bin/env python3
"""Scaffold a new app's pages (index/privacy/support) on gal-orlanczyk.github.io.

Usage:
  scripts/new_app.py --slug myapp --name "My App" \\
      --tagline "Short marketing headline." \\
      --subhead "One sentence describing what it does." \\
      --index-blurb "One line for the root apps list." \\
      --icon /path/to/icon.png

Generates <slug>/index.html, <slug>/privacy.html, <slug>/support.html from
templates/*.tmpl, copies the icon to assets/<slug>-icon.png, and adds an
entry to the root index.html's app list (skipped if the slug is already
listed there).

Review privacy.html and support.html afterwards — they're generated with
placeholder content (marked TODO) that assumes no data collection and has no
real FAQ; edit before publishing if that's not accurate for this app.
"""
import argparse
import datetime
import re
import shutil
import string
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"


def render(template_name: str, **kwargs) -> str:
    tmpl = string.Template((TEMPLATES_DIR / template_name).read_text())
    return tmpl.substitute(**kwargs)


def update_root_index(slug: str, name: str, index_blurb: str) -> None:
    index_path = REPO_ROOT / "index.html"
    html = index_path.read_text()

    if f'href="/{slug}/"' in html:
        print(f"index.html already links to /{slug}/ — leaving it as-is.")
        return

    entry = (
        f'    <li>\n'
        f'      <a href="/{slug}/">{name}</a>\n'
        f'      <p class="muted" style="margin:6px 0 0;">{index_blurb}</p>\n'
        f'    </li>'
    )
    new_html, count = re.subn(r"(\s*)</ul>", "\n" + entry + r"\1</ul>", html, count=1)
    if count == 0:
        raise SystemExit("Could not find </ul> in index.html to insert the new app entry.")
    index_path.write_text(new_html)
    print(f"Updated index.html with a link to /{slug}/.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slug", required=True, help="URL path segment, e.g. 'myapp' -> /myapp/")
    parser.add_argument("--name", required=True, help="Display name, e.g. 'My App'")
    parser.add_argument("--tagline", required=True, help="Short hero headline")
    parser.add_argument("--subhead", required=True, help="One-sentence hero description")
    parser.add_argument("--index-blurb", required=True, help="One line shown in the root apps list")
    parser.add_argument("--icon", required=True, type=Path, help="Path to a local icon image (PNG recommended)")
    parser.add_argument("--force", action="store_true", help="Overwrite the app folder if it already exists")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9-]+", args.slug):
        raise SystemExit("--slug must be lowercase letters, digits, and hyphens only.")
    if not args.icon.is_file():
        raise SystemExit(f"--icon not found: {args.icon}")

    app_dir = REPO_ROOT / args.slug
    if app_dir.exists() and not args.force:
        raise SystemExit(f"{app_dir} already exists. Pass --force to overwrite its pages.")
    app_dir.mkdir(exist_ok=True)

    icon_dest = REPO_ROOT / "assets" / f"{args.slug}-icon{args.icon.suffix}"
    icon_dest.parent.mkdir(exist_ok=True)
    shutil.copy(args.icon, icon_dest)
    if icon_dest.suffix != ".png":
        print(
            f"WARNING: icon copied as {icon_dest.name} — templates assume a .png filename "
            f"(assets/{args.slug}-icon.png). Rename the file or edit the generated HTML's <img src>."
        )

    now = datetime.datetime.now()
    substitutions = dict(
        name=args.name,
        slug=args.slug,
        tagline=args.tagline,
        subhead=args.subhead,
        year=now.year,
        month=now.strftime("%B"),
    )

    (app_dir / "index.html").write_text(render("app_index.html.tmpl", **substitutions))
    (app_dir / "privacy.html").write_text(render("app_privacy.html.tmpl", **substitutions))
    (app_dir / "support.html").write_text(render("app_support.html.tmpl", **substitutions))
    print(f"Wrote {app_dir}/index.html, privacy.html, support.html")

    update_root_index(args.slug, args.name, args.index_blurb)

    print(
        f"\nNext steps:\n"
        f"  1. Review {app_dir}/privacy.html and support.html — both have generated\n"
        f"     placeholder content (marked TODO) that assumes no data collection and\n"
        f"     has no real FAQ. Edit before publishing if that's not accurate.\n"
        f"  2. git add -A && git commit && git push\n"
    )


if __name__ == "__main__":
    sys.exit(main())
