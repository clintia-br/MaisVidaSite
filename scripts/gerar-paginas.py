#!/usr/bin/env python3
"""Gera as páginas internas do site (artigos, clínica, serviços e videx).

Cabeçalho e rodapé são extraídos do index.html, então mudar telefone, menu ou
endereço na home propaga para todas as páginas: basta rodar este script de novo.

    python3 scripts/gerar-paginas.py

Edite o TEXTO dos artigos em artigos/_conteudo/<slug>.html e os METADADOS em
artigos/artigos.json. Não edite os index.html gerados à mão: são sobrescritos.

URLs: o site usa URLs com barra final (padrão WordPress + vercel.json
trailingSlash:true). Por isso cada artigo é gerado em artigos/<slug>/index.html
e o canonical é {SITE}/artigos/<slug>/.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://www.clinicamaisvida.com"
RT = "Camilo Rodrigues Junior"
CRM = "52880299"
WA = "https://wa.me/5521983564045"
MARCA_INI = "<!-- artigos:inicio -->"
MARCA_FIM = "<!-- artigos:fim -->"

# SEO / social padrão
OG_IMG = f"{SITE}/assets/img/hero-casal-parque.jpg"
OG_IMG_W = "2752"
OG_IMG_H = "1536"
OG_IMG_ALT = "Clínica Mais Vida – Clínica Popular da Família em Nova Iguaçu (RJ)"
LOGO = f"{SITE}/wp-content/uploads/2021/06/logo-maisvida-br.png"


def bloco(html: str, tag: str) -> str:
    """Recorta <tag ...>...</tag> do índice, na primeira ocorrência."""
    ini = html.index(f"<{tag} ")
    fim = html.index(f"</{tag}>", ini) + len(f"</{tag}>")
    return html[ini:fim]


def para_subpasta(frag: str, up: str = "../") -> str:
    """Reescreve os caminhos relativos do fragmento para a profundidade dada.

    up="../" para páginas um nível abaixo da raiz (clinica/, servicos/, ...);
    up="../../" para artigos, que ficam dois níveis abaixo (artigos/<slug>/).
    """
    frag = frag.replace('href="assets/', f'href="{up}assets/')
    frag = frag.replace('src="assets/', f'src="{up}assets/')
    frag = frag.replace('href="./"', f'href="{up}"')
    for p in ("artigos", "clinica", "servicos", "videx"):
        frag = frag.replace(f'href="{p}/"', f'href="{up}{p}/"')
    return frag


def marca_ativo(frag: str, href: str) -> str:
    """Marca o item de menu da página atual."""
    return frag.replace(f'<a href="{href}">', f'<a href="{href}" aria-current="page" class="is-active">')


def escapa(txt: str) -> str:
    return txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def limpa(txt: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", txt)).strip()


def breadcrumb(itens):
    """itens: lista de (nome, url) — o último costuma ser a própria página."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": nome, "item": url}
            for i, (nome, url) in enumerate(itens, 1)
        ],
    }


def cabeca(titulo, descricao, canonical, lds=None, og_type="website",
           og_image=None, og_image_alt=None, up="../"):
    """Monta o <head> completo (SEO + social + JSON-LD) da subpágina."""
    lds = lds or []
    img = og_image or OG_IMG
    ialt = og_image_alt or OG_IMG_ALT
    # só declara dimensões quando é a imagem padrão (a única cujas medidas conhecemos)
    dims = ""
    if not og_image:
        dims = (f'<meta property="og:image:width" content="{OG_IMG_W}">\n'
                f'<meta property="og:image:height" content="{OG_IMG_H}">\n')
    ld_html = "".join(
        f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>\n'
        for x in lds)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escapa(titulo)} | Clínica Mais Vida</title>
<meta name="description" content="{escapa(descricao)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta name="author" content="Clínica Mais Vida">
<meta name="theme-color" content="#14707d">
<meta name="geo.region" content="BR-RJ">
<meta name="geo.placename" content="Nova Iguaçu, RJ">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Mais Vida - Clínica Popular da Família">
<meta property="og:title" content="{escapa(titulo)}">
<meta property="og:description" content="{escapa(descricao)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
{dims}<meta property="og:image:alt" content="{escapa(ialt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escapa(titulo)}">
<meta name="twitter:description" content="{escapa(descricao)}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="{SITE}/wp-content/uploads/2021/06/mais-vida-icone-150x150.png" sizes="32x32">
<link rel="icon" href="{SITE}/wp-content/uploads/2021/06/mais-vida-icone-300x300.png" sizes="192x192">
<link rel="apple-touch-icon" href="{SITE}/wp-content/uploads/2021/06/mais-vida-icone-300x300.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap">
<link rel="stylesheet" href="{up}assets/css/style.css?v=2">
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-KC25B9J');</script>
{ld_html}</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KC25B9J"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
"""


def rodape_extra(up: str = "../") -> str:
    return f"""
<a class="wa-float" href="{WA}" target="_blank" rel="noopener nofollow" aria-label="Falar com a clínica pelo WhatsApp">
  <svg viewBox="0 0 448 512" aria-hidden="true"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
</a>
<script src="{up}assets/js/main.js?v=2" defer></script>
</body>
</html>
"""


def main():
    indice = (RAIZ / "index.html").read_text(encoding="utf-8")
    header_raw = bloco(indice, "header")
    footer_raw = bloco(indice, "footer")
    # versões por profundidade
    cab_dir = para_subpasta(header_raw, "../")
    rod_dir = para_subpasta(footer_raw, "../")
    cab_art = para_subpasta(header_raw, "../../")
    rod_art = para_subpasta(footer_raw, "../../")
    artigos = json.loads((RAIZ / "artigos" / "artigos.json").read_text(encoding="utf-8"))

    # ----------------------------------------------------------- páginas de artigo
    for a in artigos:
        corpo = (RAIZ / "artigos" / "_conteudo" / f"{a['slug']}.html").read_text(encoding="utf-8")
        url = f"{SITE}/artigos/{a['slug']}/"
        artigo_ld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": a["titulo"],
            "description": a["resumo"],
            "image": a["imagem"],
            "datePublished": a["data"],
            "dateModified": a["data"],
            "inLanguage": "pt-BR",
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "author": {"@type": "Organization", "name": "Clínica Mais Vida", "url": f"{SITE}/"},
            "publisher": {
                "@type": "Organization",
                "name": "Clínica Mais Vida",
                "logo": {"@type": "ImageObject", "url": LOGO},
            },
        }
        crumbs_ld = breadcrumb([
            ("Início", f"{SITE}/"),
            ("Artigos", f"{SITE}/artigos/"),
            (a["titulo"], url),
        ])

        pagina = (
            cabeca(a["titulo"], a["resumo"], url, lds=[artigo_ld, crumbs_ld],
                   og_type="article", og_image=a["imagem"], og_image_alt=a["imagem_alt"],
                   up="../../")
            + cab_art
            + f"""
<main id="conteudo">
  <div class="page-head">
    <div class="container">
      <nav class="crumbs" aria-label="Você está aqui">
        <a href="../../">Início</a> &rsaquo; <a href="../">Artigos</a>
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
    <a class="btn btn-ghost" href="../">Ver todos os artigos</a>
  </div>
</main>
"""
            + rod_art
            + rodape_extra("../../")
        )
        pasta = RAIZ / "artigos" / a["slug"]
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / "index.html").write_text(pagina, encoding="utf-8")
        # remove o arquivo plano antigo, se existir (migração para pasta)
        antigo = RAIZ / "artigos" / f"{a['slug']}.html"
        if antigo.exists():
            antigo.unlink()
        print("gerado", (pasta / "index.html").relative_to(RAIZ))

    # ------------------------------------------------- cards (home e listagem)
    def card(a, prefixo="", nivel="h2", recuo=6):
        i = " " * recuo
        return f"""{i}<a class="post-card" href="{prefixo}{a['slug']}/">
{i}  <span class="post-card__cover">
{i}    <img src="{a['imagem']}" alt="{a['imagem_alt']}" loading="lazy" width="600" height="380">
{i}  </span>
{i}  <span class="post-card__body">
{i}    <span class="post-card__tag">{a['tag']}</span>
{i}    <{nivel}>{a['titulo']}</{nivel}>
{i}    <p>{a['resumo']}</p>
{i}    <span class="post-card__more">Ler artigo &rarr;</span>
{i}  </span>
{i}</a>"""

    cards = "\n".join(card(a) for a in artigos)

    # --------------------------------- seção de artigos na home (entre marcas)
    indice_txt = (RAIZ / "index.html").read_text(encoding="utf-8")
    ini = indice_txt.index(MARCA_INI) + len(MARCA_INI)
    fim = indice_txt.index(MARCA_FIM)
    home_cards = "\n".join(card(a, prefixo="artigos/", nivel="h3", recuo=8) for a in artigos[:4])
    secao_home = f"""
  <section class="posts" aria-labelledby="posts-title">
    <div class="container">
      <div class="section-divider"><span id="posts-title">Artigos e dicas de saúde</span></div>

      <div class="post-list">
{home_cards}
      </div>

      <div class="units__cta">
        <a class="btn btn-ghost" href="artigos/">Ver todos os artigos</a>
      </div>
    </div>
  </section>
  """
    (RAIZ / "index.html").write_text(indice_txt[:ini] + secao_home + indice_txt[fim:], encoding="utf-8")
    print("atualizada a seção de artigos em index.html")

    # ---------------------------------------------------- listagem de artigos
    descricao = ("Conteúdo sobre saúde, exames e especialidades da Clínica Mais Vida, "
                 "clínica popular da família em Nova Iguaçu (RJ).")
    crumbs_artigos = breadcrumb([("Início", f"{SITE}/"), ("Artigos", f"{SITE}/artigos/")])
    listagem = (
        cabeca("Artigos", descricao, f"{SITE}/artigos/", lds=[crumbs_artigos])
        + cab_dir
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
        + rod_dir
        + rodape_extra("../")
    )
    (RAIZ / "artigos" / "index.html").write_text(
        listagem.replace('href="../artigos/"', 'href="./"'), encoding="utf-8")
    print("gerado artigos/index.html")

    # ---------------------------------------------------- página da clínica
    corpo = (RAIZ / "clinica" / "conteudo.html").read_text(encoding="utf-8")
    equipe = json.loads((RAIZ / "clinica" / "equipe.json").read_text(encoding="utf-8"))

    # a coluna de registro só aparece quando TODOS estiverem preenchidos:
    # meia tabela vazia passa a impressão de descuido — ver README
    com_registro = all(m.get("registro") for m in equipe)
    cab_reg = "<th>Registro</th>" if com_registro else ""
    linhas = "\n".join(
        f"""            <tr><td>{m['nome']}</td><td>{m['especialidade']}</td>"""
        + (f"<td>{m['registro']}</td>" if com_registro else "")
        + "</tr>"
        for m in equipe)

    url_clinica = f"{SITE}/clinica/"
    desc = ("Conheça a Clínica Mais Vida: missão, visão, valores e a equipe de profissionais "
            "que atende nas unidades Cabuçu e KM 32, em Nova Iguaçu (RJ).")
    about_ld = {
        "@context": "https://schema.org", "@type": "AboutPage",
        "name": "A clínica", "description": desc, "inLanguage": "pt-BR",
        "mainEntityOfPage": url_clinica,
    }
    crumbs_clinica = breadcrumb([("Início", f"{SITE}/"), ("A clínica", url_clinica)])

    pagina = (
        cabeca("A clínica", desc, url_clinica, lds=[about_ld, crumbs_clinica])
        + marca_ativo(cab_dir, "../clinica/")
        + f"""
<main id="conteudo">
{corpo.rstrip()}

  <section class="equipe">
    <div class="container">
      <span class="rule"></span>
      <h2>conheça alguns médicos<br>de nossa equipe</h2>
      <div class="tabela-wrap">
        <table class="tabela-equipe">
          <thead>
            <tr><th>Profissional</th><th>Especialidade</th>{{cab_reg}}</tr>
          </thead>
          <tbody>
{{linhas}}
          </tbody>
        </table>
      </div>
    </div>
  </section>
</main>
""".replace("{cab_reg}", cab_reg).replace("{linhas}", linhas)
        + rod_dir
        + rodape_extra("../")
    )
    (RAIZ / "clinica" / "index.html").write_text(pagina, encoding="utf-8")
    print("gerado clinica/index.html")

    # -------------------------------------------------- página de serviços
    corpo_serv = (RAIZ / "servicos" / "conteudo.html").read_text(encoding="utf-8")
    url_serv = f"{SITE}/servicos/"
    desc_serv = ("Especialidades médicas e não médicas, exames de imagem, cardiológicos e "
                 "laboratoriais na Clínica Mais Vida, em Nova Iguaçu (RJ).")
    serv_ld = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "Exames e Serviços", "description": desc_serv, "inLanguage": "pt-BR",
        "mainEntityOfPage": url_serv,
    }
    crumbs_serv = breadcrumb([("Início", f"{SITE}/"), ("Exames e Serviços", url_serv)])

    pagina_serv = (
        cabeca("Exames e Serviços", desc_serv, url_serv, lds=[serv_ld, crumbs_serv])
        + marca_ativo(cab_dir, "../servicos/")
        + f'\n<main id="conteudo">\n{corpo_serv.rstrip()}\n</main>\n'
        + rod_dir
        + rodape_extra("../")
    )
    (RAIZ / "servicos" / "index.html").write_text(pagina_serv, encoding="utf-8")
    print("gerado servicos/index.html")

    # -------------------------------------------------- página videx
    corpo_videx = (RAIZ / "videx" / "conteudo.html").read_text(encoding="utf-8")
    url_videx = f"{SITE}/videx/"
    desc_videx = ("Videx: planos de benefícios para 3, 4 ou 5 pessoas, com consultas, descontos "
                  "em exames, terapias e medicamentos na Clínica Mais Vida, em Nova Iguaçu (RJ).")
    videx_ld = {
        "@context": "https://schema.org", "@type": "WebPage",
        "name": "Videx", "description": desc_videx, "inLanguage": "pt-BR",
        "mainEntityOfPage": url_videx,
    }
    crumbs_videx = breadcrumb([("Início", f"{SITE}/"), ("Videx", url_videx)])
    pagina_videx = (
        cabeca("Videx", desc_videx, url_videx, lds=[videx_ld, crumbs_videx])
        + marca_ativo(cab_dir, "../videx/")
        + f'\n<main id="conteudo">\n{corpo_videx.rstrip()}\n</main>\n'
        + rod_dir
        + rodape_extra("../")
    )
    (RAIZ / "videx" / "index.html").write_text(pagina_videx, encoding="utf-8")
    print("gerado videx/index.html")


if __name__ == "__main__":
    main()
