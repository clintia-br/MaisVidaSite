# Mais Vida — Clínica Popular da Família (site estático)

Versão estática da home de [clinicamaisvida.com](https://www.clinicamaisvida.com/):
HTML + CSS + JS puros, **sem WordPress, sem Elementor, sem plugins**.
Abre direto no navegador e publica em qualquer host estático (Vercel, GitHub Pages, Netlify, Cloudflare Pages).

```
index.html                  home completa (header, hero, unidades, avaliações, rodapé)
assets/css/style.css        todo o CSS do site
assets/js/main.js           carrossel, slideshows, menu mobile, aviso de cookies
assets/img/                 vazio hoje — ver "Imagens" abaixo
artigos/                    blog: index gerado + páginas dos artigos
artigos/_conteudo/          texto dos artigos (é isto que se edita)
artigos/artigos.json        título, resumo, tag e data de cada artigo
scripts/baixar-imagens.sh   traz as imagens do WordPress para assets/img/
scripts/gerar-artigos.py    monta as páginas de artigo a partir do conteúdo
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

## Artigos e FAQ

**FAQ** fica na home, acima das avaliações, em `<section class="faq">`. São 8 perguntas em
`<details>` nativo — abre e fecha sem JavaScript. O mesmo conteúdo está marcado como
`FAQPage` no JSON-LD, o que ajuda o Google a entender as respostas.

**Artigos** ficam em `artigos/`, com um mini-sistema sem dependência nenhuma:

```
artigos/artigos.json        metadados (título, resumo, tag, data, leitura, capa)
artigos/_conteudo/*.html    o texto de cada artigo — só o miolo, sem cabeçalho
artigos/*.html              páginas prontas — GERADAS, não edite à mão
```

Para publicar ou alterar um artigo:

```bash
# 1. edite artigos/_conteudo/<slug>.html e/ou artigos/artigos.json
# 2. regenere as páginas
python3 scripts/gerar-artigos.py
# 3. acrescente a URL nova ao sitemap.xml e faça commit
```

O gerador copia o cabeçalho e o rodapé do `index.html`, então **mudou o telefone ou o menu
na home, rode o script de novo** e todas as páginas acompanham. Ele também reescreve a seção
"Artigos e dicas de saúde" da home, entre as marcas `<!-- artigos:inicio -->` e
`<!-- artigos:fim -->` — não edite esse trecho à mão.

### Capas dos artigos

Cada artigo tem `imagem` e `imagem_alt` no `artigos.json`. Para trocar, aponte para o arquivo
novo e rode o gerador.

⚠️ **As capas atuais são provisórias.** Não consegui obter fotos novas, então reaproveitei
fotos que a clínica já tem no WordPress — e três delas **já aparecem em outras seções da home**
(o bloco de fisioterapia e os cards de unidade). Fica repetido. Peça ao cliente 4 capas
próprias, ou fotos do acervo da clínica que ainda não estejam no site.

Ao escolher, siga o DPV: *"Imagens de procedimento não são utilizadas. Registro de ambiente e
de equipe é o recurso visual padrão."* Ou seja: ambiente da clínica e equipe, não banco de
imagens genérico de procedimento médico. Cada artigo sai com JSON-LD
`Article`, breadcrumb, CTA de WhatsApp e o aviso de que o conteúdo não substitui consulta.

### De onde veio esse conteúdo

Fonte principal: o **DPV — Dossiê de Posicionamento e Vendas da Clínica Mais Vida**
(versão 2.0, agosto/2026, `dpvmaisvida.vercel.app`). Dele saíram os preços, a grade de
especialidades por unidade, o vocabulário permitido, a checagem de conformidade e as pautas.
O plano de conteúdo de setembro/2026 (Drive, pasta "22. Clínica Mais Vida") complementou o
registro de escrita.

O que o DPV determina e está aplicado aqui:

- **Preço aparece.** "A clínica é favorável à transparência de preço." A regra é informar o
  valor sem comparar com terceiros e sem apelo promocional.
- **Vocabulário.** Use: "consulta a partir de R$ 120", "sem plano de saúde", "aqui no bairro",
  "exame na própria clínica", "resultado pelo WhatsApp", "para toda a família", "acompanhamento".
  Nunca use: "cura garantida", "o melhor médico", "único da cidade", "mais barato que a
  concorrência", "antes e depois", "sem dor", "promoção".
- **Nunca anuncie especialidade indisponível numa unidade.** O DPV é explícito: isso é
  propaganda enganosa, faz o paciente se deslocar à toa e gera avaliação negativa numa ficha
  do Google que ainda não tem histórico para absorver.

### Valores que NÃO devem ser publicados ainda

O próprio DPV marca como pendente de confirmação — por isso ficaram fora do FAQ:

- **Pilates** (R$ 105 e R$ 170): falta confirmar se é mensal ou por sessão.
- **RPG**: o pacote de 5 sessões (R$ 400) está acima de 5 sessões avulsas (R$ 375).
- **Plano da clínica / Videx**: valor individual, familiar, cobertura, dependentes e carências
  estão listados como "a confirmar". O Instagram publica "a partir de R$ 199,90/mês", mas o
  DPV não confirma — por isso o FAQ cita o plano sem preço.

### Divergências encontradas — alguém precisa decidir

- **Horário de sábado.** O site diz 7h30–12h; o DPV diz 7h–12h nas duas unidades. Mantivemos
  7h30 (o que já estava publicado). Confirme qual é o certo: errar isso faz o paciente chegar
  na porta fechada.
- **WhatsApp do KM 32.** O DPV registra que a unidade só tem telefone fixo e que é preciso
  habilitar um número móvel antes das campanhas. Enquanto isso, o FAQ manda o KM 32 para o
  telefone, não para o WhatsApp.

### Ainda faltam respostas do cliente

- formas de pagamento e condições de parcelamento
- política de retorno (está incluso? em qual prazo?)
- prazo de entrega dos resultados de exame — aparece como crítica numa avaliação do Google

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

A nota (4,7) e o total (1.565) são estáticos. Revise de tempos em tempos ou combine com o
cliente uma frase que não envelheça ("mais de 1.500 avaliações").

## Antes de publicar: aprovação

**Cássia é a responsável única pela aprovação de todo material de marketing**, site incluído
(definido no DPV). O conteúdo médico passa também pelo responsável técnico, Dr. Camilo
Rodrigues Junior (CRM 52880299).

A checagem do DPV, aplicada a tudo que está aqui:

- [x] sem promessa de cura, de resultado ou de superioridade
- [x] sem antes e depois
- [x] sem linguagem sensacionalista, superlativo absoluto ou escassez artificial
- [x] preço em caráter informativo, sem comparação e sem apelo promocional
- [x] depoimentos tratam de experiência de atendimento, nunca de resultado de tratamento
- [x] especialidades anunciadas correspondem ao que cada unidade atende
- [ ] **autorização registrada** para as avaliações de paciente exibidas na home — pendente

### Sugestões do DPV que ainda não estão no site

O DPV pede que o site tenha, além do que já existe:

1. **Páginas por unidade**, com endereço e mapa.
2. **Páginas por especialidade**, com preço informativo.
3. **Página de exames.**

E aponta três diferenciais que os pacientes citam sozinhos nas avaliações e que **não estão em
nenhuma peça atual**: o resultado de exame enviado por WhatsApp, o cafezinho de cortesia na
recepção e o fato de a clínica atender a família inteira. O primeiro já entrou no FAQ; os
outros dois valem uma passada na home.

## Ajustes rápidos

| O quê | Onde |
|---|---|
| Cores da marca | `assets/css/style.css`, bloco `:root` |
| Telefones / WhatsApp | buscar por `wa.me` e `tel:` no `index.html` |
| Textos do carrossel | `index.html`, seção `<!-- HERO -->` |
| Velocidade do carrossel | `assets/js/main.js`, constante `DELAY` |
| Tempo dos slideshows | atributo `data-interval` no `index.html` |
