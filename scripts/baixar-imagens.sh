#!/usr/bin/env bash
# Baixa as imagens que hoje são carregadas do WordPress para assets/img/
# e reescreve o index.html para usar os arquivos locais.
#
# Rode a partir da raiz do repositório:  bash scripts/baixar-imagens.sh
set -euo pipefail

BASE="https://www.clinicamaisvida.com/wp-content/uploads"
DEST="assets/img"
mkdir -p "$DEST"

ARQUIVOS=(
  "2026/07/logo-clinica-mais-vida.webp"
  "2026/08/seja-videx.png"
  "2026/07/senior-woman-with-stretch-band-being-assist-by-female-physiotherapist.webp"
  "2026/07/people-taking-pilates-reformer-class.webp"
  "2026/07/woman-rehabilitation-center-getting-treatment.webp"
  "2024/06/recepcao-mais-vidas-004.jpg"
  "2024/08/mais-vida-002.jpeg"
  "2024/08/mais-vida-001.jpeg"
  "2024/04/fachada-clinica-mais-vidas-001.jpeg"
  "2021/06/logo-maisvida-br.png"
  "2021/06/mais-vida-icone-150x150.png"
  "2021/06/mais-vida-icone-300x300.png"
)

for caminho in "${ARQUIVOS[@]}"; do
  nome="$(basename "$caminho")"
  echo "baixando $nome"
  curl -fsSL "$BASE/$caminho" -o "$DEST/$nome"
done

echo "reescrevendo caminhos no index.html"
python3 - <<'PY'
import re

UP = r'https://www\.clinicamaisvida\.com/wp-content/uploads/\d{4}/\d{2}/'
html = open('index.html', encoding='utf-8').read()

def local(m):
    """Troca a URL do WordPress pelo arquivo local, mantendo o delimitador."""
    return m.group(1) + 'assets/img/' + m.group(2)

# Só reescreve onde o navegador carrega o arquivo: src="", url('') e data-images.
# JSON-LD, og:image e canonical continuam com URL absoluta (exigido por buscadores).
html = re.sub(r'(src=")' + UP + r'([^"]+)', local, html)
html = re.sub(r"(url\(')" + UP + r"([^']+)", local, html)
html = re.sub(r'(href=")' + UP + r'([^"]+\.(?:png|webp|jpe?g|ico))', local, html)  # favicons
html = re.sub(
    r"data-images='\[.*?\]'",
    lambda m: re.sub(UP + r'([^"]+)', lambda x: 'assets/img/' + x.group(1), m.group(0)),
    html,
    flags=re.S,
)

open('index.html', 'w', encoding='utf-8').write(html)
PY
echo "pronto. confira o site e faça commit de assets/img/ + index.html"
