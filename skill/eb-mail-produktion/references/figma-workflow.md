# Figma-Workflow (EB-Mails-Static)

- **Einzige Arbeitsdatei:** „EB-Mails-Static“ `<FIGMA_FILE_KEY>`, Page „E-Mails“ `0:1`, Page „Statics“ `1:2`. Figma-Account mit Zugriff auf die Datei (Professional-Plan mit Full Seat; auf Starter sperrt das MCP nach ~12 Calls).
- Mail-Frames 1080 breit, Export immer ×1.5 → 1620 px.
- Master-Library „EMAIL-SYSTEM-LIBRARY“ `<LIBRARY_FILE_KEY>`.

## Node-Zugriff
- Immer per `findOne(n => n.name === '…' && n.type === '…')`, nie IDs aus Positionslisten raten.
- Text ändern mit Erhalt der Bold-Bereiche: Fonts laden (`getRangeAllFontNames`), dann `insertCharacters(i+old.length, neu, 'BEFORE')` + `deleteCharacters(i, i+old.length)`. Danach Höhe vergleichen (kein neuer Umbruch), auto-width-Texte neu zentrieren: `x = (parent.width - width)/2`.
- Auto-Height-Text: erst `characters`, dann `resize(w, t.height)`.
- Section-Shift: alle Kinder mit `y >= cut - 5` verschieben, Frame + ggf. Hero mit `resize` vergrößern. Hero-Bereich vergrößern statt Motiv in die Fades zu quetschen.

## Bilder hochladen (Workaround für Zahlen-Parameter-Bug)
1. `upload_assets` mit `fileKey` + `currentPageId` **ohne `count`** → liefert genau 1 `submitUrl`.
2. `curl -s -X POST -F "file=@bild.jpg;type=image/jpeg" "<submitUrl>"` → `imageHash` + `placedOnNodeId`.
3. Fill tauschen: `n.fills = n.fills.map(f => f.type==='IMAGE' ? {...f, imageHash: H} : f)`; Temp-Node `placedOnNodeId` löschen.
- `figma.createImageAsync` und `loadAllPagesAsync` sind NICHT verfügbar (`page.loadAsync()` nutzen).

## Export (Workaround: `defaultScale` als Zahl scheitert)
```js
// TMP-Frames pro Mail, je ≤ 2600 hoch, geklont und ×1.5 skaliert
const H=Math.round(m.height), n=Math.ceil(H/2600), cuts=[...Array(n+1)].map((_,i)=>Math.round(H*i/n));
for (let i=0;i<n;i++){ const f=figma.createFrame(); f.name='TMP-export-…'; f.resize(1080,cuts[i+1]-cuts[i]);
  f.x=128000+i*1700; f.y=-4873; f.clipsContent=true; f.fills=[{type:'SOLID',color:{r:11/255,g:11/255,b:13/255}}];
  figma.currentPage.appendChild(f); const c=m.clone(); f.appendChild(c); c.x=0; c.y=-cuts[i]; f.rescale(1.5); }
```
- Dann `download_assets` mit `nodeId` (einzeln, nicht `nodeIds`) + `format: png` → URL per curl laden.
- Nur geänderte Teile neu exportieren (spart Figma-Calls), mit `scripts/stitch_parts.py` zusammensetzen.
- Danach ALLE `TMP-`-Frames löschen.
- QA immer über `download_assets`-Export, nicht `get_screenshot` (rendert Fades falsch).
