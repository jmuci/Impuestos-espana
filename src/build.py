"""Genera ../index.html a partir de style.css, body.html (con la pestaña 7 de tab8.py) y app.js."""
import sys
from pathlib import Path

here = Path(__file__).parent
sys.path.insert(0, str(here))
import tab8
import cotiz
head = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>¿Quién paga los impuestos en España?</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..500&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<style>
'''
css = (here / 'style.css').read_text(encoding='utf-8')
body = (here / 'body.html').read_text(encoding='utf-8').replace('{{TAB8}}', tab8.html()).replace('{{COTIZ}}', cotiz.html())
js = (here / 'app.js').read_text(encoding='utf-8')
out = head + css + '</style>\n</head>\n<body>\n\n' + body + '\n<script>\n' + js + '</script>\n</body>\n</html>\n'
(here.parent / 'index.html').write_text(out, encoding='utf-8')
print(len(out.splitlines()), 'lines')
