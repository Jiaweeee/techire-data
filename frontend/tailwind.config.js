/** @type {import('tailwindcss').Config} */
import typography from '@tailwindcss/typography'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            'h2': {
              marginTop: '2rem',
              marginBottom: '1rem',
            },
            'ul': {
              marginTop: '1rem',
              marginBottom: '1rem',
            },
          }
        }
      },
      maxWidth: {
        '7xl': '80rem',
      },
    },
  },
  plugins: [
    typography(),
  ],
};
