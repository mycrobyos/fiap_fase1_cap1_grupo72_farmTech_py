# FarmTech Solutions – Agricultura Digital (FIAP)

Aplicação **Python + R** para apoiar a migração à Agricultura Digital.
Atende aos requisitos: duas culturas, cálculo de área, manejo de insumos,
dados em vetores, menu completo (CRUD + cálculos + export), loops e decisões,
e estatística básica em R.

## Culturas e Geometria
- **Café**: área calculada como **retângulo** (largura × comprimento).
- **Soja**: área calculada como **círculo** (π · raio²).

## Manejo de Insumos
Para qualquer cultura: o insumo total é `dose (mL/m) × comprimento de rua (m) × nº de ruas`, convertido para **litros**.

## Estrutura
- `farmtech.py` — CLI em Python (dados em **vetores/listas**).
- `stats.R` — Estatística básica em R a partir do CSV exportado.
- `parcelas.csv` — (gerado pela aplicação) base com as parcelas.

## Como rodar (Python)
Requer Python 3.10+.
```bash
python3 farmtech.py
```
Menu oferece:
1. Inserir parcela
2. Listar parcelas
3. Atualizar por ID
4. Deletar por ID
5. Calcular áreas por cultura
6. Calcular insumos
7. Exportar CSV para R
8. Sair

> Dica: use a opção 7 para gerar `parcelas.csv`.

## Como rodar (R)
No R:
```r
setwd("CAMINHO/DA/PASTA")
source("stats.R")           # usa parcelas.csv por padrão
# ou pela linha de comando:
# Rscript stats.R parcelas.csv
```

Saída esperada: média e desvio-padrão de área (m²) e insumo (L), geral e por cultura.

## GitHub (trabalho em equipe)
Fluxo sugerido:
1. **Fork** do repositório (ou um dono cria e adiciona colaboradores).
2. Cada pessoa cria uma **branch**: `feat/ui-cli`, `feat/soja`, `fix/calculo-insumo`, etc.
3. Commits pequenos e claros:
   - `git add .`
   - `git commit -m "feat: menu CRUD completo"`
   - `git push origin feat/ui-cli`
4. **Pull Request** para `main`, com revisão de colegas.
5. Use **Issues** para dividir tarefas e **Projects** para Kanban.
6. A cada mudança aprovada, **merge** em `main` + **tag** de versão (ex.: `v1.0.0`).

## Ideias de extensão
- Persistência em JSON/SQLite.
- Novas culturas e geometrias.
- Cálculo de custo (R$/L) por produto.
- Relatórios gráficos (matplotlib/ggplot2).
