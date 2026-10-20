# Fontes dos recursos visuais

O perfil apresenta a experiência e a formação documentadas no [currículo profissional](https://www.pmoraes.dev.br/curriculo).

- **Logos de tecnologias:** [Devicon](https://github.com/devicons/devicon), revisão `6a37858047b0e8d9c9c0e68f4a071fc410652e89`. MIT; os nomes e logos pertencem às respectivas marcas.
- **MCP:** [Simple Icons](https://github.com/simple-icons/simple-icons), revisão `c71c69e3a27e4436936b831c72643e6513b9f49b`. CC0.
- **dbt:** [arquivo oficial de documentação](https://github.com/dbt-labs/docs.getdbt.com/blob/f5c4986033cfae8c93a1367d6e98fefd479045b0/website/static/img/dbt-logo.svg). O símbolo é extraído do lockup horizontal, sem redesenho. [Diretrizes da marca](https://www.getdbt.com/dbt-assets/dbt-trademark-guidelines).
- **Ícones de interface e conceitos:** [Lucide](https://lucide.dev/), revisão `c29c276f16590cf017126671535ad8c792be64d8`, licença ISC. LLM e RAG usam ícones conceituais.
- **Tipografia da capa:** [IBM Plex Mono](https://www.ibm.com/plex/), arquivos de [Google Fonts](https://github.com/google/fonts/tree/47d54ca1ebb14fd864695f1d39dc734f39017c33/ofl/ibmplexmono).
- **Tipografia dos identificadores:** [Manrope](https://fonts.google.com/specimen/Manrope), arquivo variável de [Google Fonts](https://github.com/google/fonts/tree/47d54ca1ebb14fd864695f1d39dc734f39017c33/ofl/manrope).

As fontes usam a SIL Open Font License. As licenças ficam em `assets/licenses/`. O manifesto `assets/sources.json` registra a origem e o SHA-256 de cada arquivo original.

## Regeneração

Dependências: Python com Pillow, Node.js com sharp.

```sh
python scripts/fetch-design-assets.py
node scripts/render-icons.cjs
python scripts/generate-profile.py
python scripts/generate-banner.py
```

Os identificadores PNG têm resolução dupla e versões claras e escuras. A capa animada também oferece uma versão estática para movimento reduzido. Os recursos finais são servidos pelo próprio repositório.
