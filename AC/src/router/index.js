import { createRouter, createWebHistory } from 'vue-router'

const routes = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: () => import('../pages/Home.vue')
        },
        {
            path: '/:pathMatch(.*)*',
            redirect: '/'
        }
    ],
})

export default routes