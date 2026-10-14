# coding: utf-8
"""Build standalone Pages entry and downloadable source archive; standard library only."""
from pathlib import Path
import base64, json, re, zipfile
root=Path(__file__).resolve().parent
src=root/'source'/'dist'
css=(src/'style.css').read_text()
css=re.sub(r"url\('([^']+\.woff2)'\)",lambda m:"url('data:font/woff2;base64,"+base64.b64encode((src/m[1]).read_bytes()).decode()+"')",css)
js=(src/'app.js').read_text()
data=json.loads((src/'sources.json').read_text())
js=js.replace("fetch('sources.json').then(r=>{if(!r.ok)throw Error('Библиотека недоступна');return r.json();})",'Promise.resolve('+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+')')
html=(src/'index.html').read_text().replace('<link rel="stylesheet" href="style.css">','<style>'+css+'</style>').replace('<script src="app.js" defer></script>','<script>'+js+'</script>')
html=html.replace('href="icon.svg"','href="data:image/svg+xml;base64,'+base64.b64encode((src/'icon.svg').read_bytes()).decode()+'"')
(root/'index.html').write_text(html)
with zipfile.ZipFile(root/'source-code.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((root/'source').rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root))
 z.write(root/'build-site.py','build-site.py')
 for name in ['PRODUCT.md','DESIGN.md','.impeccable/design.json','.impeccable/surfaces/research-cabinet.md']:
  if (root/name).is_file():z.write(root/name,name)
print('Built index.html and source-code.zip:',len(data),'sources')
