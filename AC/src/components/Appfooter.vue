<script setup>
const currentYear = new Date().getFullYear()

const footerSections = [
  {
    title: 'Servizi',
    links: [
      { name: 'Servizi', href: '/servizi' },
      { name: 'Consulenza', href: '#' },
      { name: 'Sviluppo Web', href: '#' },
    ],
  },
  {
    title: 'Azienda',
    links: [
      { name: 'About', href: '/about' },
    ],
  },
  {
    title: 'Legale',
    links: [
      { name: 'Privacy Policy', href: '#' },
      { name: 'Cookie Policy', href: '#' },
      { name: 'Termini di Servizio', href: '#' },
    ],
  },
]
</script>

<template>
  <!-- FULL WIDTH FOOTER -->
  <footer class="w-full bg-white border-t border-gray-100">

    <!-- CONTENT WRAPPER (CENTRATO MA NON LIMITANTE) -->
    <div class="w-full px-6 lg:px-10 py-12 lg:py-16">

      <!-- GRID -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-12">

        <!-- BRAND -->
        <div class="lg:col-span-2 space-y-4">

          <a href="/" class="text-xl font-bold tracking-tight text-green-900">
            Emotional<span class="text-red-800"> Journal</span>
          </a>

          <p class="text-sm text-gray-500 max-w-sm leading-relaxed">
            Keep your emotions journal up to date.
          </p>

          <!-- SOCIAL -->
          <div class="flex space-x-5 text-gray-400">

            <a href="https://github.com/manuelrovitti/Affective_Computer.git" class="hover:text-gray-900 transition-colors">
              <span class="sr-only">GitHub</span>

              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 .5C5.73.5.75 5.62.75 12c0 5.1 3.29 9.43 7.86 10.96.58.11.79-.26.79-.58v-2.05c-3.2.71-3.88-1.37-3.88-1.37-.53-1.37-1.29-1.73-1.29-1.73-1.05-.74.08-.73.08-.73 1.16.08 1.77 1.22 1.77 1.22 1.03 1.82 2.7 1.29 3.36.98.1-.77.4-1.29.73-1.59-2.55-.3-5.23-1.31-5.23-5.83 0-1.29.44-2.35 1.17-3.18-.12-.3-.51-1.51.11-3.14 0 0 .96-.31 3.14 1.21a10.6 10.6 0 0 1 2.86-.39c.97 0 1.94.13 2.86.39 2.18-1.52 3.14-1.21 3.14-1.21.62 1.63.23 2.84.11 3.14.73.83 1.17 1.89 1.17 3.18 0 4.53-2.69 5.52-5.25 5.82.41.36.78 1.08.78 2.18v3.23c0 .32.21.69.8.57A10.77 10.77 0 0 0 23.25 12C23.25 5.62 18.27.5 12 .5z"/>
              </svg>
            </a>

            <a href="https://www.linkedin.com/in/manuel-rovitti-35b498258/" class="hover:text-blue-400 transition-colors">
              <span class="sr-only">LinkedIn</span>
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.779-1.75-1.75s.784-1.75 1.75-1.75 1.75.779 1.75 1.75-.784 1.75-1.75 1.75zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
              </svg>
            </a>

          </div>
        </div>

        <!-- LINK SECTIONS -->
        <div
          v-for="section in footerSections"
          :key="section.title"
          class="space-y-4"
        >
          <h3 class="text-xs font-semibold text-gray-400 tracking-wider uppercase">
            {{ section.title }}
          </h3>

          <ul class="space-y-2.5">
            <li v-for="link in section.links" :key="link.name">
              <a
                :href="link.href"
                class="text-sm text-gray-600 hover:text-blue-900 transition-colors duration-150"
              >
                {{ link.name }}
              </a>
            </li>
          </ul>
        </div>

      </div>

      <!-- BOTTOM BAR -->
      <div
        class="mt-12 pt-8 border-t border-gray-100 flex flex-col sm:flex-row justify-between items-center gap-4"
      >
        <p class="text-xs text-gray-400">
          &copy; {{ currentYear }} Emotional Journal. Tutti i diritti riservati.
        </p>

        <p class="text-xs text-gray-400 tracking-wide">
          P.IVA 01234567890
        </p>
      </div>

    </div>
  </footer>
</template>