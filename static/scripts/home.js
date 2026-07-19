
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
        disableOnInteraction: false,
    },

    navigation: {
        nextEl: "#homeswiper-button-next",
        prevEl: "#homeswiper-button-prev",
    },
})


const category_carousel = new Swiper('.category-carousel' , {
    slidesPerView: 9,
    spaceBetween: 10,

    speed: 3000,
    freeMode: true,
    loop: true,
    autoplay: {
        delay: 0,
        waitForTransition: true,
    },

    navigation: {
        nextEl: "#category-carousel-button-next",
        prevEl: "#category-carousel-button-prev",
    },

    breakpoints: {
        300: {
            slidesPerView: 2.5
        },
        500: {
            slidesPerView: 3
        },
        600: {
            slidesPerView: 4
        },
        700: {
            slidesPerView: 5
        },
        800: {
            slidesPerView: 6
        },
        900: {
            slidesPerView: 7
        },
        1000: {
            slidesPerView: 8
        },
        1160: {
            slidesPerView: 9
        }
    }

})

let btn_carousel_category = document.getElementById('btn-carousel-category')
btn_carousel_category.addEventListener('click' ,()=> {
    if (window.innerWidth > 1130) {
        Menu('cat' ,null)
    } else {
        SideMenu('open' ,'cat-sidemenu')
    }
})