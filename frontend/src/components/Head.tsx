import { Helmet } from 'react-helmet-async';

interface HeadProps {
  title?: string;
  description?: string;
  canonical?: string;
  image?: string;
  type?: 'website' | 'article' | 'job';
}

export function Head({ 
  title, 
  description,
  canonical,
  image = 'https://realtechjobs.com/social-share.png', // TODO: replace with real image
  type = 'website'
}: HeadProps) {
  const siteTitle = 'RealTechJobs';
  const fullTitle = title ? `${title} | ${siteTitle}` : siteTitle;
  const defaultDescription = 'Find fresh tech jobs directly from company career pages. Real opportunities, no third-party recruiters.';
  const finalDescription = description || defaultDescription;

  return (
    <Helmet>
      {/* 基础 Meta 标签 */}
      <title>{fullTitle}</title>
      <meta name="description" content={finalDescription} />
      {canonical && <link rel="canonical" href={canonical} />}

      {/* Open Graph 标签 */}
      <meta property="og:site_name" content={siteTitle} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={finalDescription} />
      <meta property="og:type" content={type} />
      {canonical && <meta property="og:url" content={canonical} />}
      <meta property="og:image" content={image} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />

      {/* Twitter Cards 标签 */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site" content="@RealTechJobs" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={finalDescription} />
      <meta name="twitter:image" content={image} />
    </Helmet>
  );
} 