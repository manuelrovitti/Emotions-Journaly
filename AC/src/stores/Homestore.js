import { defineStore } from 'pinia'
import image1 from '../assets/Sfondo1.jpg'
import bg from '../assets/bg.jpg'

export const useSiteStore = defineStore('site', () => {

    const heroImages = [
        image1,
    ]

    const bgImage = bg

    return {
        heroImages,
        bgImage
    }
})