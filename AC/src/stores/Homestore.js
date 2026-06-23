import { defineStore } from 'pinia'
import image1 from '../assets/Sfondo1.jpg'


export const useSiteStore = defineStore('site', () => {

    const heroImages = [
        image1,
    ]

    return {
        heroImages,
    }
})