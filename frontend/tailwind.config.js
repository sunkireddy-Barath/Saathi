/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#4F46E5",
        secondary: "#10B981",
        background: "#0F172A",
        surface: "#1E293B",
        textMain: "#F8FAFC",
        textMuted: "#94A3B8",
        danger: "#EF4444",
        warning: "#F59E0B",
      },
      fontFamily: {
        sans: ["System", "sans-serif"],
      },
    },
  },
  plugins: [],
};
