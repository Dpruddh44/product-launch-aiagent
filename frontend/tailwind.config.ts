import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          50: '#fdf8f3',
          100: '#faefd9',
          200: '#f4ddb3',
          300: '#edc482',
          400: '#e5a64f',
          500: '#d4921d',
          600: '#b87a15',
          700: '#976214',
          800: '#7c5117',
          900: '#674318',
        },
      },
    },
  },
  plugins: [],
};
export default config;
