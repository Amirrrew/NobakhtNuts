
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

const article_carousel = new Swiper('#article-swiper' , {
    slidesPerView: 4,
    spaceBetween: 10,
    navigation: {
        nextEl: '#btn-article-carousel-next',
        prevEl: '#btn-article-carousel-prev',
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
            slidesPerView: 2.1
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


const why_nobakht_swiper = new Swiper('#why-nobakht-swiper' , {
    slidesPerView: 4,
    spaceBetween: 10,
    navigation: {
        nextEl: '#card-swiper-button-next',
        prevEl: '#card-swiper-button-prev',
    },
    speed: 500,
    autoplay: {
        delay: 2000,
    },

    breakpoints: {
        300: {
            slidesPerView: 1.2
        },
        800: {
            slidesPerView: 2.2
        },
        1050: {
            slidesPerView: 4
        },
        1500: {
            slidesPerView: 4
        },
        1800: {
            slidesPerView: 4
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
