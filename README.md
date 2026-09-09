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
`.github/workflows/deploy-pages.yml` publica a cada push.

> O repositório foi criado vazio, então o GitHub marcou `claude/clinica-mais-vida-site-g9zarc`
> como branch padrão. Vale renomear para `main` em _Settings → Branches_ (e aí simplificar
> a lista `branches:` do workflow).

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

**3. Estilo remontado à mão.** O CSS do Elementor não pôde ser baixado (mesma restrição de
rede — a URL era um hash do LiteSpeed, que muda a cada limpeza de cache), então o layout foi
refeito a partir da estrutura do HTML e calibrado por captura de tela do site no ar:
teal `#14707D` + rosa `#E61A67`, faixa rosa de diferenciais, faixa verde do "Associe-se",
rodapé teal com os cards de agenda em branco. Tons finos podem ser ajustados em `:root`
no `style.css`.

**4. Foto da unidade KM 32.** A URL não estava no HTML enviado, então o card usa
um fundo na cor da marca. Coloque a foto em `assets/img/` e troque
`unit-card--brand` por `data-slideshow data-images='["assets/img/arquivo.jpg"]'`.

**5. Créditos "Desenvolvido por GeDê"** foram mantidos como no site atual — remover é decisão de vocês.

## Avaliações do Google

O site antigo usava o widget da Trustindex (JS externo, puxava as avaliações ao vivo).
Aqui elas são **estáticas**, com a marca do Google reproduzida em SVG/CSS — nada de script
de terceiros, nada para carregar.

- **O texto é literal**, exatamente como está publicado no Google, inclusive a ressalva sobre
  demora nos resultados de exames. Não edite nem recorte avaliação de paciente: além de
  enganoso, é o tipo de coisa que derruba a credibilidade do bloco.
- **As datas se calculam sozinhas** ("há 2 meses") a partir do `datetime` de cada `<time>`;
  sem JS, aparece a data absoluta. Não precisa mexer com o tempo passando.
- **Para atualizar:** edite os `<blockquote class="review">` no `index.html` — nome, `datetime`,
  texto e a URL da foto em `--photo`. Atualize também o total em `.reviews__count` e no botão.
- **"Leia mais"** aparece sozinho só quando o texto foi cortado.

⚠️ **CFM 2336/2023:** depoimento de paciente em site de clínica precisa de validação do
responsável técnico (Dr. Camilo Rodrigues Junior, CRM 52880299) antes de publicar — mesmo
já estando no ar hoje. Para tirar, apague o bloco `<section class="reviews">` do `index.html`.

## Ajustes rápidos

| O quê | Onde |
|---|---|
| Cores da marca | `assets/css/style.css`, bloco `:root` |
| Telefones / WhatsApp | buscar por `wa.me` e `tel:` no `index.html` |
| Textos do carrossel | `index.html`, seção `<!-- HERO -->` |
| Velocidade do carrossel | `assets/js/main.js`, constante `DELAY` |
| Tempo dos slideshows | atributo `data-interval` no `index.html` |
