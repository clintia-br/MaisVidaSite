#!/usr/bin/env python3
"""Gera as páginas de artigo a partir do conteúdo em artigos/_conteudo/.

Cabeçalho e rodapé são extraídos do index.html, então mudar telefone, menu ou
endereço na home propaga para todos os artigos: basta rodar este script de novo.

    python3 scripts/gerar-artigos.py

Edite o TEXTO dos artigos em artigos/_conteudo/<slug>.html e os METADADOS em
artigos/artigos.json. Não edite artigos/<slug>.html à mão: é gerado e será
sobrescrito.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://www.clinicamaisvida.com"
RT = "Camilo Rodrigues Junior"
CRM = "52880299"
WA = "https://wa.me/5521983564045"


def bloco(html: str, tag: str) -> str:
    """Recorta <tag ...>...</tag> do índice, na primeira ocorrência."""
    ini = html.index(f"<{tag} ")
    fim = html.index(f"</{tag}>", ini) + len(f"</{tag}>")
    return html[ini:fim]


def para_subpasta(frag: str) -> str:
    """Reescreve os caminhos relativos do fragmento para a pasta artigos/."""
    frag = frag.replace('href="assets/', 'href="../assets/')
    frag = frag.replace('src="assets/', 'src="../assets/')
    frag = frag.replace('href="./"', 'href="../"')
    frag = frag.replace('href="artigos/"', 'href="./"')
    return frag


def escapa(txt: str) -> str:
    return txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def limpa(txt: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", txt)).strip()


def cabeca(titulo, descricao, canonical, extra_ld=""):
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escapa(titulo)} | Clínica Mais Vida</title>
<meta name="description" content="{escapa(descricao)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{escapa(titulo)}">
<meta property="og:description" content="{escapa(descricao)}">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="{SITE}/wp-content/uploads/2021/06/mais-vida-icone-150x150.png" sizes="32x32">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap">
<link rel="stylesheet" href="../assets/css/style.css">
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-KC25B9J');</script>
{extra_ld}</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KC25B9J"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
"""


RODAPE_EXTRA = """
<a class="wa-float" href="{wa}" target="_blank" rel="noopener nofollow" aria-label="Falar com a clínica pelo WhatsApp">
  <svg viewBox="0 0 448 512" aria-hidden="true"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
</a>
<script src="../assets/js/main.js" defer></script>
</body>
</html>
""".format(wa=WA)


def main():
    indice = (RAIZ / "index.html").read_text(encoding="utf-8")
    cabecalho = para_subpasta(bloco(indice, "header"))
    rodape = para_subpasta(bloco(indice, "footer"))
    artigos = json.loads((RAIZ / "artigos" / "artigos.json").read_text(encoding="utf-8"))

    # ---------------------------------------------------------------- páginas
    for a in artigos:
        corpo = (RAIZ / "artigos" / "_conteudo" / f"{a['slug']}.html").read_text(encoding="utf-8")
        url = f"{SITE}/artigos/{a['slug']}/"
        ld = json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": a["titulo"],
            "description": a["resumo"],
            "datePublished": a["data"],
            "dateModified": a["data"],
            "inLanguage": "pt-BR",
            "mainEntityOfPage": url,
            "author": {"@type": "Organization", "name": "Clínica Mais Vida"},
            "publisher": {"@type": "Organization", "name": "Clínica Mais Vida"},
        }, ensure_ascii=False, indent=2)

        pagina = (
            cabeca(a["titulo"], a["resumo"], url,
                   f'<script type="application/ld+json">\n{ld}\n</script>\n')
            + cabecalho
            + f"""
<main id="conteudo">
  <div class="page-head">
    <div class="container">
      <nav class="crumbs" aria-label="Você está aqui">
        <a href="../">Início</a> &rsaquo; <a href="./">Artigos</a>
      </nav>
      <h1>{a['titulo']}</h1>
    </div>
  </div>

  <article class="post">
    <div class="container">
      <div class="post__body">
        <div class="post__meta">
          <span>{a['tag']}</span>
          <time datetime="{a['data']}">{a['data_legivel']}</time>
          <span>{a['leitura']} de leitura</span>
        </div>

{corpo.rstrip()}

        <div class="post__cta">
          <h2>Precisa de atendimento?</h2>
          <p>Consultas, exames e 19 especialidades nas unidades Cabuçu e KM 32, em Nova Iguaçu.</p>
          <a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener nofollow">Agendar pelo WhatsApp</a>
        </div>

        <div class="disclaimer">
          <p>Este conteúdo tem caráter informativo e não substitui a consulta, o diagnóstico ou o
          tratamento indicado por um profissional de saúde. Procure sempre orientação médica.
          Responsável técnico: {RT} &ndash; CRM {CRM}.</p>
        </div>
      </div>
    </div>
  </article>

  <div class="post-nav">
    <a class="btn btn-ghost" href="./">Ver todos os artigos</a>
  </div>
</main>
"""
            + rodape
            + RODAPE_EXTRA
        )
        destino = RAIZ / "artigos" / f"{a['slug']}.html"
        destino.write_text(pagina, encoding="utf-8")
        print("gerado", destino.relative_to(RAIZ))

    # ----------------------------------------------------------------- índice
    cards = "\n".join(f"""      <a class="post-card" href="{a['slug']}.html">
        <span class="post-card__tag">{a['tag']}</span>
        <h2>{a['titulo']}</h2>
        <p>{a['resumo']}</p>
        <span class="post-card__more">Ler artigo &rarr;</span>
      </a>""" for a in artigos)

    descricao = ("Conteúdo sobre saúde, exames e especialidades da Clínica Mais Vida, "
                 "clínica popular da família em Nova Iguaçu (RJ).")
    listagem = (
        cabeca("Artigos", descricao, f"{SITE}/artigos/")
        + cabecalho
        + f"""
<main id="conteudo">
  <div class="page-head">
    <div class="container">
      <nav class="crumbs" aria-label="Você está aqui"><a href="../">Início</a> &rsaquo; Artigos</nav>
      <h1>Artigos</h1>
      <p>Informação sobre saúde, exames e especialidades, para você entender melhor o seu cuidado.</p>
    </div>
  </div>

  <div class="container">
    <div class="post-list">
{cards}
    </div>
  </div>
</main>
"""
        + rodape
        + RODAPE_EXTRA
    )
    (RAIZ / "artigos" / "index.html").write_text(listagem, encoding="utf-8")
    print("gerado artigos/index.html")


if __name__ == "__main__":
    main()
