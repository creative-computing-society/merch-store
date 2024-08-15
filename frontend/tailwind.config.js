/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{js,jsx,ts,tsx}', './index.html'],
  theme: {
    extend: {
      colors: {
        primary: '#353831',
        primaryHover: '#494b45',
        container: '#f8f8f8',
      }
    },
  },
  plugins: [],
}

