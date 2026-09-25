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

Tudo vem do bloco `RELATORIO` no começo do `<script>` do `index.html`:

- `periodo` — datas do chip do cabeçalho.
- `meta.campanhas[]` — por campanha: `cliques` (Resultados = cliques no link),
  `investido` (Valor gasto), `verbaDia`, `alcance`, `impressoes`.
  `semResultado: true` para campanha sem resultado no período (entra só no investimento).
- `google.campanhas[]` — por campanha, somando os dias do export:
  `impressoes`, `cliques`, `investido` (Custo), `leads` (Conversões), `verbaDia`.
  `situacao: "aprendizado"` marca campanha quase sem veiculação.
- `google.termos[]` — termos de busca que geraram lead.
- `destaques[]` — os três cards de leitura para o cliente (`tipo`: `sky`, `""`, `grey`).
- `selo: "hot"` destaca a campanha líder; `situacao: "pausado"` acinzenta.

Números puros com ponto decimal (`58.03`). `null` = sem dado (a página mostra "—").
KPIs, gráficos, tabelas, totais, custo por clique/lead e o parágrafo de abertura
são calculados na hora — nenhum número é digitado duas vezes.

Passos: exportar Meta (nível campanha) e Google (Pesquisa, por palavra-chave),
salvar os CSVs em `dados/`, somar o Google por campanha, preencher o bloco,
escrever os destaques, subir a `versao` (`v2`, `v3`…), abrir o HTML e conferir.

## Compliance

Relatório interno / de gestão para o cliente (Daniel), não é peça voltada ao
paciente. Não há claim clínico nem preço; não exige gate CFM 2336/2023.
