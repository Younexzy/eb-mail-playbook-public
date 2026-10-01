#!/bin/bash
# Installiert das Playbook: Skill per Symlink (Repo = Master), optional Gedächtnis (Ordner memory/, privat), Preflight.
set -e
R="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p ~/.claude/skills
SK=~/.claude/skills/eb-mail-produktion
if [ -e "$SK" ] && [ ! -L "$SK" ]; then mkdir -p ~/.claude/backups; mv "$SK" ~/.claude/backups/eb-mail-produktion.bak-$(date +%Y%m%d%H%M); echo "Alte Skill-Kopie nach ~/.claude/backups verschoben"; fi
ln -sfn "$R/skill/eb-mail-produktion" "$SK"; echo "✓ Skill verlinkt"
install_mem() {  # $1 = Projektordner, für den Claude das Gedächtnis laden soll
  local key; key=$(echo "$1" | sed 's#[/.]#-#g'); local MEM=~/.claude/projects/$key/memory; mkdir -p "$MEM"; local n=0
  for f in "$R"/memory/*.md; do b=$(basename "$f"); [ "$b" = MEMORY.md ] && continue; [ -e "$MEM/$b" ] || { cp "$f" "$MEM/"; n=$((n+1)); }; done
  if [ ! -e "$MEM/MEMORY.md" ]; then cp "$R/memory/MEMORY.md" "$MEM/"; else
    while IFS= read -r line; do f=$(echo "$line" | sed -n 's/.*(\([^)]*\.md\)).*/\1/p'); [ -n "$f" ] && ! grep -q "($f)" "$MEM/MEMORY.md" && echo "$line" >> "$MEM/MEMORY.md"; done < "$R/memory/MEMORY.md"; fi
  echo "✓ Gedächtnis für $1: $n Dateien ergänzt"
}
if [ -d "$R/memory" ]; then install_mem "$R"; fi
echo; python3 "$R/skill/eb-mail-produktion/scripts/preflight.py" || true
echo; echo "Nächster Schritt: In der Claude-App (Code-Tab) den Ordner $R öffnen."
