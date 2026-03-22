/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['DM Sans', 'system-ui', 'sans-serif'],
        display: ['Playfair Display', 'serif'],
      },
      colors: {
        skin: {
          primary: '#0D9488',
          accent: '#14B8A6',
          muted: '#99F6E4',
          dark: '#0F766E',
          cream: '#FFFBEB',
          warm: '#FEF3C7',
        },
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(13, 148, 136, 0.1), 0 2px 8px -2px rgba(0,0,0,0.06)',
        'card': '0 10px 40px -10px rgba(13, 148, 136, 0.15)',
      },
    },
  },
  plugins: [],
}
