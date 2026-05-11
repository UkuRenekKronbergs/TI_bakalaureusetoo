/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        kindlus: {
          korge: "#15803d",
          keskmine: "#ca8a04",
          madal: "#6b7280",
        },
      },
    },
  },
  plugins: [],
};
