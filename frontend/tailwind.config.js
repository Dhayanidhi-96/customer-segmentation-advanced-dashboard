export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#141414',
        cream: '#faf6ef',
        moss: '#4f7c55',
        coral: '#f06b4f',
        amber: '#f7b538',
      },
      fontFamily: {
        display: ['Sora', 'sans-serif'],
        body: ['Manrope', 'sans-serif'],
      },
      backgroundImage: {
        aura: 'radial-gradient(circle at 20% 15%, rgba(240,107,79,0.2), transparent 40%), radial-gradient(circle at 80% 15%, rgba(79,124,85,0.2), transparent 40%)',
      },
    },
  },
  plugins: [],
}
