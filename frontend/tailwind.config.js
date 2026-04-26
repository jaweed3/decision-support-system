/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#020617', // slate-950
        primary: '#22d3ee',    // cyan-400
        secondary: '#8b5cf6',  // violet-500
        accent: '#f472b6',     // pink-400
      },
      boxShadow: {
        'neon': '0 0 5px theme("colors.primary"), 0 0 20px theme("colors.primary")',
      }
    },
  },
  plugins: [],
}
