import fs from 'node:fs';
import path from 'node:path';
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Existe um package-lock.json na pasta do utilizador; fixa a raiz neste projeto.
  outputFileTracingRoot: path.join(__dirname),
  images: {
    // 1440 e 1600 entre os tamanhos de ecrã: num portátil o hero deixa de
    // descarregar a versão de 1920 px.
    deviceSizes: [640, 750, 828, 1080, 1200, 1440, 1600, 1920, 2048, 3840],
    formats: ['image/avif', 'image/webp'],
    // A partir do Next 15 só são servidas as qualidades declaradas aqui.
    // 75 é o valor por omissão; 90 é o dos screenshots dos trabalhos, onde
    // se lê texto pequeno e a compressão nota-se.
    qualities: [75, 90],
  },
  async rewrites() {
    // Site v5: todas as páginas são HTML estático em public/, em PT e EN,
    // geradas a partir do protótipo validado (ver site-v5/README.md).
    // A lista vem de site-v5/paginas.json. beforeFiles: ganham às rotas React,
    // que ficam só para artigos novos do blog ainda sem versão estática e para o 404.
    const paginas: string[] = JSON.parse(fs.readFileSync(path.join(__dirname, 'site-v5/paginas.json'), 'utf8'));
    return {
      beforeFiles: [
        { source: '/', destination: '/inicio/index.html' },
        ...paginas.map((p) => ({ source: `/${p}`, destination: `/${p}/index.html` })),
      ],
      afterFiles: [
        // O painel Decap e uma pagina estatica em public/admin/.
        { source: '/admin', destination: '/admin/index.html' },
        // Cartão digital do Web Summit, página estática em public/card/.
        { source: '/card', destination: '/card/index.html' },
      ],
      fallback: [],
    };
  },
  async redirects() {
    return [
      // IA privada passou a chamar-se Assistente interno (30/10/2026).
      { source: '/ia-privada', destination: '/assistente-interno', statusCode: 301 },
      // O HTML de base não deve ser indexado pelo seu endereço interno.
      { source: '/inicio', destination: '/', statusCode: 301 },
      // URLs do protótipo estático → rotas limpas.
      { source: '/index.html', destination: '/', statusCode: 301 },
      { source: '/websites.html', destination: '/websites', statusCode: 301 },
      { source: '/lojas-online.html', destination: '/lojas-online', statusCode: 301 },
      { source: '/automacoes.html', destination: '/automacoes', statusCode: 301 },
      { source: '/metodo.html', destination: '/metodo', statusCode: 301 },
      { source: '/sobre.html', destination: '/sobre', statusCode: 301 },
      { source: '/blog.html', destination: '/blog', statusCode: 301 },
      { source: '/trabalho-ubi.html', destination: '/trabalhos/ubi', statusCode: 301 },
      { source: '/trabalho-ubi', destination: '/trabalhos/ubi', statusCode: 301 },
      { source: '/trabalho-planet-trading.html', destination: '/trabalhos/planet-trading', statusCode: 301 },
      { source: '/trabalho-planet-trading', destination: '/trabalhos/planet-trading', statusCode: 301 },
      { source: '/trabalho-studyos.html', destination: '/trabalhos/studyos', statusCode: 301 },
      { source: '/trabalho-studyos', destination: '/trabalhos/studyos', statusCode: 301 },

      // URLs do site anterior, retirados do sitemap.xml e das ligações internas
      // de starmountainflash.pt em 23/09/2026.
      { source: '/servicos/sistemas-digitais', destination: '/websites', statusCode: 301 },
      { source: '/servicos/automatizacoes', destination: '/automacoes', statusCode: 301 },
      { source: '/servicos', destination: '/#servicos', statusCode: 301 },
      { source: '/privacy', destination: '/privacidade', statusCode: 301 },
      // Endereços do site anterior que o Search Console ainda mostrava em 09/10/2026.
      { source: '/privacy.html', destination: '/privacidade', statusCode: 301 },
      { source: '/blog-designed-to-be-cited.html', destination: '/blog', statusCode: 301 },
      { source: '/servicos/websites.html', destination: '/websites', statusCode: 301 },
      { source: '/servicos/automatizacao-ia.html', destination: '/automacoes', statusCode: 301 },
      { source: '/terms', destination: '/termos', statusCode: 301 },
      // Ainda com impressões no Search Console em 14/10/2026.
      { source: '/terms.html', destination: '/termos', statusCode: 301 },
      // /aviso-legal, /cookies, /blog e /blog/quando-automatizar-o-teu-negocio
      // continuam a existir com o mesmo endereço: não precisam de redirecionamento.
    ];
  },
};

export default nextConfig;
