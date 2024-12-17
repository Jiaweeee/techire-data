import { Helmet } from 'react-helmet-async';

interface HeadProps {
  title?: string;
  description?: string;
  canonical?: string;
}

export function Head({ 
  title, 
  description,
  canonical
}: HeadProps) {
  const siteTitle = 'RealTechJobs';
  const fullTitle = title ? `${title} | ${siteTitle}` : siteTitle;
  const defaultDescription = 'Find fresh tech jobs directly from company career pages. Real opportunities, no third-party recruiters.';

  return (
    <Helmet>
      <title>{fullTitle}</title>
      <meta name="description" content={description || defaultDescription} />
      {canonical && <link rel="canonical" href={canonical} />}
    </Helmet>
  );
} 