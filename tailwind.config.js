/** Tailwind-konfiguration.
 *
 * Sajten laddade tidigare cdn.tailwindcss.com, som kompilerar CSS i
 * webblasaren vid varje sidvisning. Det ar render-blockerande och kostar
 * bade laddningstid och Core Web Vitals. Nu byggs CSS:en en gang hit:
 *
 *   make css
 *
 * Kor det efter att ha lagt till nya klasser i en sida, annars saknas de.
 */
module.exports = {
  content: ["./static/**/*.html", "./templates/*.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["'Plus Jakarta Sans'", "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
};
