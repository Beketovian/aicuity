/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      gridTemplateColumns: {
        'playlist': '1fr 200px 80px'
      },
      boxShadow: {
        "brutalist": "2px 3px rgba(0, 0, 0, 1)",
      }
    },
  },
  plugins: [],
}