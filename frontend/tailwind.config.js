/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        krishi: {
          primary: "#237A45",
          dark: "#164B32",
          light: "#EAF5EC",
          bg: "#F7FAF7",
          text: "#26352B",
          warning: "#E6A23C",
          danger: "#D9534F",
          accent: "#38A169"
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

