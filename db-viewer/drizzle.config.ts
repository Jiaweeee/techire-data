import { defineConfig } from 'drizzle-kit'

const dialect = (() => {
  const url = process.env.DATABASE_URL || '';
  if (url.includes('mysql')) return 'mysql' as const;
  if (url.includes('postgres') || url.includes('postgresql')) return 'postgresql' as const;
  if (url.includes('sqlite')) return 'sqlite' as const;
  if (url.includes('turso')) return 'turso' as const;
  throw new Error('Unsupported database URL');
})();

export default defineConfig({
  dialect,
  ...(dialect === 'mysql' || dialect === 'postgresql' || dialect === 'sqlite' || dialect === 'turso' 
    ? { dbCredentials: { url: process.env.DATABASE_URL || '' } }
    : {})
})