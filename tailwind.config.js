/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6200EE',
          dark: '#BB86FC',
        },
        secondary: {
          DEFAULT: '#03DAC6',
          dark: '#03DAC6',
        },
        error: {
          DEFAULT: '#B00020',
          dark: '#CF6679',
        },
        success: {
          DEFAULT: '#00C853',
          dark: '#69F0AE',
        },
        warning: {
          DEFAULT: '#FFDE03',
          dark: '#FFD740',
        },
      },
      animation: {
        fadeIn: 'fadeIn 0.3s ease-in-out',
        pulse: 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0, transform: 'translateY(10px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            code: {
              color: theme('colors.pink.600'),
              backgroundColor: theme('colors.gray.100'),
              padding: '0.1rem 0.3rem',
              borderRadius: '0.25rem',
              fontWeight: '400',
            },
            'code::before': {
              content: '""',
            },
            'code::after': {
              content: '""',
            },
            h1: {
              marginTop: '1.5rem',
              marginBottom: '1rem',
            },
            h2: {
              marginTop: '1.3rem',
              marginBottom: '0.8rem',
            },
            h3: {
              marginTop: '1.2rem',
              marginBottom: '0.6rem',
            },
            h4: {
              marginTop: '1.1rem',
              marginBottom: '0.5rem',
            },
            p: {
              marginTop: '0.5rem',
              marginBottom: '0.5rem',
            },
            li: {
              marginTop: '0.25rem',
              marginBottom: '0.25rem',
            },
          },
        },
      }),
    },
  },
  plugins: [],
};