# Mais Vida — Clínica Popular da Família (site estático)

Versão estática da home de [clinicamaisvida.com](https://www.clinicamaisvida.com/):
HTML + CSS + JS puros, **sem WordPress, sem Elementor, sem plugins**.
Abre direto no navegador e publica em qualquer host estático (Vercel, GitHub Pages, Netlify, Cloudflare Pages).

```
index.html                  home completa (header, hero, unidades, avaliações, rodapé)
assets/css/style.css        todo o CSS do site
assets/js/main.js           carrossel, slideshows, menu mobile, aviso de cookies
assets/img/                 vazio hoje — ver "Imagens" abaixo
scripts/baixar-imagens.sh   traz as imagens do WordPress para assets/img/
vercel.json                 cache dos assets + headers de segurança
.github/workflows/          deploy automático no GitHub Pages
robots.txt / sitemap.xml    SEO básico
```

## Rodar localmente

```bash
python3 -m http.server 8000
# abre http://localhost:8000
```

Abrir o `index.html` com duplo clique também funciona.

## Publicar

**Vercel (recomendado):** _New Project_ → importar este repositório → framework **Other**,
sem build command, output = raiz. O `vercel.json` já está pronto.

**GitHub Pages:** _Settings → Pages → Source: GitHub Actions_. O workflow
`.github/workflows/deploy-pages.yml` publica a cada push na `main`.

> Ao apontar o domínio para cá, atualize o `canonical`, o `og:url` e o `sitemap.xml`
> se o endereço final não for `https://www.clinicamaisvida.com/`.

## O que já está funcionando

- Carrossel do topo com 3 slides (autoplay 5s, setas, bolinhas, swipe no celular, pausa no hover).
- Slideshows de fundo (fisioterapia e unidade Cabuçu) com pré-carregamento das imagens.
- Menu mobile, header sticky, botão flutuante de WhatsApp.
- GTM `GTM-KC25B9J` e GA4 `GT-NCLXB4J8` — mesmos IDs do site atual.
- Verificação de domínio da Meta mantida (`facebook-domain-verification`).
- Aviso de cookies simples (LGPD), com escolha guardada no `localStorage`.
- Dados estruturados `MedicalClinic` (JSON-LD) para as duas unidades — endereço,
  telefone e horários. **Isso não existia no site antigo** e ajuda no Google/GMB.
- `alt` descritivo nas imagens, skip-link, foco visível, `prefers-reduced-motion`.

## Pendências conhecidas

**1. Imagens ainda vêm do WordPress.** O ambiente onde este código foi gerado não tinha
acesso de rede a `clinicamaisvida.com`, então as imagens são carregadas por URL absoluta
de `/wp-content/uploads/`. Elas aparecem normalmente, mas o site depende do WordPress no ar.
Para resolver, na sua máquina:

```bash
bash scripts/baixar-imagens.sh
git add assets/img index.html && git commit -m "imagens locais" && git push
```

**2. Páginas internas.** Só a home foi enviada. Os links do menu (`clínica`, `nossos serviços`,
`videx`, `contato`), `especialidades` e `política de privacidade` apontam para as URLs
atuais em `www.clinicamaisvida.com` — nada quebra, mas o visitante sai deste site.
Manda o HTML dessas páginas que eu converto do mesmo jeito.

**3. Estilo aproximado em alguns pontos.** O CSS do Elementor não pôde ser baixado
(mesma restrição de rede — a URL era um hash do LiteSpeed, que muda a cada limpeza de cache).
O layout foi remontado a partir da estrutura do HTML. Confirmado do original: rosa `#E61A67`.
Os demais tons (azul `#123B6B`, cinzas) são aproximações — ajuste em `:root` no `style.css`.

**4. Foto da unidade KM 32.** A URL não estava no HTML enviado, então o card usa
um fundo na cor da marca. Coloque a foto em `assets/img/` e troque
`unit-card--brand` por `data-slideshow data-images='["assets/img/arquivo.jpg"]'`.

**5. Créditos "Desenvolvido por GeDê"** foram mantidos como no site atual — remover é decisão de vocês.

## Avaliações e CFM 2336/2023

A seção "O que nossos pacientes dizem" reproduz avaliações públicas do Google que **já estão
publicadas no site atual** (widget Trustindex). Conteúdo com depoimento de paciente em site
de clínica precisa de validação sob a **Resolução CFM 2336/2023** antes de ir ao ar —
valide com o responsável técnico (Dr. Camilo Rodrigues Junior, CRM 52880299) antes de publicar.
Para tirar do ar, apague o bloco `<section class="reviews">` do `index.html`.

## Ajustes rápidos

| O quê | Onde |
|---|---|
| Cores da marca | `assets/css/style.css`, bloco `:root` |
| Telefones / WhatsApp | buscar por `wa.me` e `tel:` no `index.html` |
| Textos do carrossel | `index.html`, seção `<!-- HERO -->` |
| Velocidade do carrossel | `assets/js/main.js`, constante `DELAY` |
| Tempo dos slideshows | atributo `data-interval` no `index.html` |
