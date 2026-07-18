
const homeswiper = new Swiper('.home-swiper' , {
    slidesPerView: 1,
    spaceBetween: 0,

    pagination: {
        el: '.homeswiper-pagination',
        clickable: true ,
    },

    speed: 500,

    autoplay: {
        delay: 4000,
        disableOnIntraction: false,
    },

    navigation: {
        nextEl: "#homeswiper-button-next",
        prevEl: "#homeswiper-button-prev",
    },
})
