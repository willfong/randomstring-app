/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/templates/**/*.html",
    "./src/templates/**/*.jinja",
    "./src/templates/**/*.jinja2",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#f59e0b',
      }
    }
  },
  plugins: [],
}
