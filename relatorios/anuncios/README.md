# Relatório de mídia — Clínica Mais Vida (Meta Ads + Google Ads)

Página isolada do site: um único `index.html`, sem `assets/css` nem `assets/js`,
identidade ClintIA (mesmo modelo do relatório do Centro Médico 3 Elementos).
Não é linkada do menu, tem `noindex, nofollow`, está fora do `sitemap.xml` e
bloqueada no `robots.txt`. Publica junto com o site em `/relatorios/anuncios/`.

```
index.html   relatório (dados + renderização no mesmo arquivo)
dados/       exports originais que alimentaram cada versão
```

## Como atualizar

Tudo vem do bloco `RELATORIO` no começo do `<script>` do `index.html`.
A página tem um seletor de mês e, dentro de cada mês, as abas Visão geral,
Meta Ads, Google Ads e Comparativo mensal (variação automática entre meses).

`meses[]` guarda um bloco por mês, o mais recente primeiro. Para um mês novo,
copie o bloco anterior e troque `id` (AAAA-MM), `label`, `sub`, `chip`, `status`
e os números. Dentro de cada mês:

- `meta.campanhas[]` — por campanha: `cliques` (Resultados = cliques no link),
  `investido` (Valor gasto), `verbaDia`, `alcance`, `impressoes`.
  `semResultado: true` para campanha sem resultado no período (entra só no investimento).
- `google.campanhas[]` — por campanha, somando os dias do export:
  `impressoes`, `cliques`, `investido` (Custo), `leads` (Conversões), `verbaDia`.
  `situacao: "aprendizado"` marca campanha quase sem veiculação.
- `google.termos[]` — termos de busca que geraram lead.
- `meta.insights[]` e `google.insights[]` — leitura por canal (`tipo`: `good`, `""`, `warn`).
- `destaques[]` — os três cards de leitura para o cliente (`tipo`: `sky`, `""`, `grey`).
- `selo: "hot"` destaca a campanha líder; `situacao: "pausado"` acinzenta.

Números puros com ponto decimal (`58.03`). `null` = sem dado (a página mostra "—").
KPIs, gráficos, tabelas, totais, custo por clique/lead, o parágrafo de abertura
e o comparativo mensal são calculados na hora — nenhum número é digitado duas vezes.

## Origem dos meses de 2026

Meta: o export de campanhas cobre 26/08–24/09; os meses foram contados pelos
dias de veiculação de cada um (agosto 26–31/08, setembro 01–24/09). Google:
export por palavra-chave e dia, 22–25/09.

Google Ads não veiculou em agosto (`google.campanhas: []` + `semVeiculacao`);
a página mostra a aba com o motivo em vez de tabelas vazias.

Passos: exportar Meta (nível campanha) e Google (Pesquisa, por palavra-chave),
salvar os CSVs em `dados/`, somar o Google por campanha, preencher o bloco,
escrever os destaques, subir a `versao` (`v2`, `v3`…), abrir o HTML e conferir.

## Compliance

Relatório interno / de gestão para o cliente (Daniel), não é peça voltada ao
paciente. Não há claim clínico nem preço; não exige gate CFM 2336/2023.
