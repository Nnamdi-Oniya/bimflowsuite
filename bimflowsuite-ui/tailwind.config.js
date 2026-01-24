/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enables dark mode via 'dark' class on html/body
  theme: {
    extend: {
      colors: {
        // 🌈 Brand Colors (yours—love 'em!)
        magenta: '#FF00FF',         // Primary accent (vibrant)
        onion: '#6A0DAD',           // Deep brand purple
        orchid: '#DA70D6',          // Soft complementary tone
        violet: '#8A2BE2',          // Secondary accent for highlights
        dark: '#0F0A1C',            // Background dark tone
        light: '#F5F5F5',           // Text & base light tone
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 4px 10px rgba(0, 0, 0, 0.15)',
        glow: '0 0 20px rgba(106, 13, 173, 0.6)', // Onion-inspired glow
      },
    },
  },
  plugins: [require('@tailwindcss/typography')], // For rich text in reviews
};