
const homeswiper = new Swiper('.home-swiper' , {
    slidesPerView: 'auto',
    spaceBetween: 10,
    centeredSlides: true,
    loop: true,

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

    },


    breakpoints: {
        300: {
            slidesPerView: 2.2
        },
        400: {
            slidesPerView: 2.5
        },
        500: {
            slidesPerView: 3
        },
        600: {
            slidesPerView: 3
        },
        700: {
            slidesPerView: 3
        },
        800: {
            slidesPerView: 4
        },
        900: {
            slidesPerView: 5
        },
        1000: {
            slidesPerView: 6
        },
        1160: {
            slidesPerView: 7
        },
        1300: {
            slidesPerView: 9
        }
    }

})

let btn_carousel_category = document.getElementById('btn-carousel-category')
btn_carousel_category.addEventListener('click' ,()=> {
    if (window.innerWidth > 1130) {
        CategoryMenu(true)
    } else {
        SideMenu('open' ,'cat-sidemenu')
    }
})

const special_carousel = new Swiper('.special-carousel' , {
    slidesPerView: 3,
    spaceBetween: 10,
    navigation: {
        nextEl: '.btn-special-carousel-next',
        prevEl: '.btn-special-carousel-prev',
    },
    speed: 500,
    autoplay: {
        delay: 3000,
        waitForTransition: true,
    },

    breakpoints: {
        300: {
            slidesPerView: 1.1
        },
        800: {
            slidesPerView: 1.5
        },
        1050: {
            slidesPerView: 2
        },
        1500: {
            slidesPerView: 2.5
        },
        1800: {
            slidesPerView: 3.5
        }
    }

})

function initScrollAnimation(options = {}) {
    const {
        selector = '.animate-on-scroll',
        activeClass = 'active',
        threshold = 0.2,
        rootMargin = '0px 0px -200px 0px',
        once = true
    } = options;

    const elements = document.querySelectorAll(selector);

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add(activeClass);

                if (once) {
                    observer.unobserve(entry.target);
                }
            } else if (!once) {
                entry.target.classList.remove(activeClass);
            }
        });
    }, {
        threshold: threshold,
        rootMargin: rootMargin
    });

    elements.forEach(el => observer.observe(el));

    return observer
}


initScrollAnimation();

const card_block_swiper = new Swiper('#card-block' , {
    slidesPerView: 3.5,
    spaceBetween: 10,
    navigation: {
        nextEl: '#card-swiper-button-next',
        prevEl: '#card-swiper-button-prev',
    },
    speed: 500,
    autoplay: {
        delay: 2000,
        waitForTransition: true,
        pauseOnMouseEnter: true,
    },

    breakpoints: {
        300: {
            slidesPerView: 1.1
        },
        800: {
            slidesPerView: 1.3
        },
        1050: {
            slidesPerView: 2.5
        },
        1500: {
            slidesPerView: 3.5
        },
        1800: {
            slidesPerView: 4.5
        }
    }

})

function initSwiperScrollAutoplay(options = {}) {
    const {
        selector = '.swiper',
        threshold = 0.2,
        rootMargin = '0px 0px -100px 0px',
        once = true
    } = options;

    const sliderElements = document.querySelectorAll(selector);

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const swiperInstance = entry.target.swiper;
            if (!swiperInstance) return;

            if (entry.isIntersecting) {
                swiperInstance.autoplay.start();

                if (once) {
                    observer.unobserve(entry.target);
                }
            } else if (!once) {
                swiperInstance.autoplay.stop();
            }
        });
    }, {
        threshold: threshold,
        rootMargin: rootMargin
    });

    sliderElements.forEach(el => {
        if (el.swiper) {
            el.swiper.autoplay.stop();   // اول متوقفش کن
            observer.observe(el);
        }
    });

    return observer;
}

initSwiperScrollAutoplay();