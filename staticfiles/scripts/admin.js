let loader = document.getElementById('loader')
let sidebar = document.querySelector('.sidebar-admin')
// نمایش دکمه اسکرول تو تاپ سایدبار
sidebar.addEventListener('scroll' ,()=> {
    if (sidebar.scrollTop > 20) {
        document.getElementById('sidebar-backtotop').style = 'bottom: 30px;'
    } else {document.getElementById('sidebar-backtotop').style = 'bottom: -200px'}
})


// مدیریت ساید بار
let admin_header = document.getElementById('admin-header')
let admin_content = document.getElementById('admin-content')
let admin_profile = document.getElementById('admin-profile')
let admin_sidebar = document.getElementById('admin-sidebar')

let sidebar_collapsed = localStorage.getItem('sidebar') === 'collapsed';

let applySidebarState = () => {
    if (sidebar_collapsed) {
        admin_header.style.width = 'calc(100vw - 40px)';
        admin_content.style.marginRight = '20px';
        admin_profile.style.marginRight = '-1000px';
        admin_sidebar.style.marginRight = '-1000px';
    } else {
        admin_header.style.width = 'calc(100vw - 400px)';
        admin_content.style.marginRight = '380px';
        admin_profile.style.marginRight = '20px';
        admin_sidebar.style.marginRight = '20px';
    }
}

applySidebarState();

function AdminSideAction() {
    sidebar_collapsed = !sidebar_collapsed;
    localStorage.setItem(
        'sidebar',
        sidebar_collapsed ? 'collapsed' : 'expanded'
    );
    applySidebarState();
}


// پاپ آپ نوتیفیکیشن
let PopUpNotif = (type ,action) => {
    let parent = document.getElementById('popup-parent-pop-notif')
    let popup = document.getElementById('popup-form-notif')

    if (action === 'open') {
        window.innerWidth > 1130 ? parent.style = 'display: flex; align-items:center;' :parent.style = 'display: flex; align-items:end;'
        document.body.style.overflowY = 'hidden'
        window.innerWidth < 1130 ? popup.style = 'animation: popup-mobile 300ms': null
        setTimeout(() => {
            document.addEventListener('click', popupClickHandler)
        }, 200)
    } else {
        window.innerWidth < 1130 ? popup.style = 'animation: popup-mobile-close 300ms' : popup.style = 'animation: unload4 200ms'
        setTimeout(()=> {
            parent.style = 'display: none'
            popup.style = 'animation: load5 300ms;'
            document.body.style.overflowY = 'scroll'
            document.removeEventListener('click', popupClickHandler)
        } ,100)
    }
}



// لیست گزینه های پنل ادمین
const admin_options = [
    {title: 'خانه' ,url: '/adminpanel/'},
    {title: 'آمار فروش' ,url: '/adminpanel/sales-stats/'},
    {title: 'سفارشات' ,url: '/adminpanel/orders/'},
    {title: 'محصولات' ,url: '/adminpanel/products/'},
    {title: 'افزودن محصول جدید' ,url: '/adminpanel/products/add/'},
    {title: 'شاخه های اصلی' ,url: '/adminpanel/main-categories/'},
    {title: 'افزودن شاخه اصلی' ,url: '/adminpanel/main-categories/add/'},
    {title: 'زیر شاخه ها' ,url: '/adminpanel/sub-categories/'},
    {title: 'افزودن زیر شاخه' ,url: '/adminpanel/sub-categories/add/'},
    {title: 'بسته بندی ها' ,url: '/adminpanel/packs/'},
    {title: 'افزودن بسته بندی جدید' ,url: '/adminpanel/packs/add'},
    {title: 'برند ها' ,url: '/adminpanel/brands/'},
    {title: 'افزودن برند جدید' ,url: '/adminpanel/brands/add'},
    {title: 'کامنت ها' ,url: '/adminpanel/comments/'},
    {title: 'کاربران' ,url: '/adminpanel/users/'},
    {title: 'افزودن کاربر جدید' ,url: '/adminpanel/users/add'},
    {title: 'مقالات' ,url: '/adminpanel/'},
    {title: 'افزودن مقاله جدید' ,url: '/adminpanel/'},
    // {title: 'تیکت های پشتیبانی' ,url: '/adminpanel/'},
    {title: 'راه های ارتباطی' ,url: '/adminpanel/support-ways/'},
    {title: 'افزودن راه ارتباطی' ,url: '/adminpanel/support-ways/add/'},
    {title: 'تنظیمات سایت' ,url: '/adminpanel/sitesettings/'},
    {title: 'دسته بندی فوتر لینک' ,url: '/adminpanel/footerlinks/'},
    {title: 'افزودن دسته بندی فوتر لینک' ,url: '/adminpanel/footerlinks/'},
    {title: 'فوتر لینک ها' ,url: '/adminpanel/footerlinks/'},
    {title: 'افزودن فوتر لینک' ,url: '/adminpanel/footerlinks/add'},
    {title: 'کارت های بانکی من' ,url: '/adminpanel/cards/'},
    {title: 'افزودن کارت بانکی جدید' ,url: '/adminpanel/cards/add'},
    {title: 'نرخ و روش های ارسال' ,url: '/adminpanel/posting-fees/'},
]




let admin_searchbox = document.querySelector('.admin-searchbox')
let admin_search_input = document.getElementById('admin-search')
let admin_search_result = document.getElementById('admin-searchresult')

// اضافه کردن ایونت لیستنر روی سرچ باکس برای بسته باز و بسته شدن سرچ باکس
document.addEventListener("click", (e) => {
    if (!admin_searchbox.contains(e.target)) {
        admin_searchbox.style = "height: 50px;";
    }
});

//انجام سرچ پنل ادمین
let AdminSearch = () => {
    const value = admin_search_input.value.trim().toLowerCase();
    const results = admin_options.filter(option =>
        option.title.toLowerCase().includes(value)
    );
    if (results.length > 0) {
        admin_searchbox.style = `height: ${(results.length + 1) * 55 < 500 ? (results.length +1) * 55 : '500' }px;`
        let rescontent = ``;
        for (let sr = 0; sr < results.length; sr++) {
            let res = results[sr]
            rescontent += `
                <a href="${res.url}" class="flex relative justify-between py-3 px-3 mx-3 rounded-xl cursor-pointer transition-all hover:bg-[var(--color12)]">
                    <h1>${res.title}</h1>
                    <i class="fa fa-angle-left mt-1 text-[var(--color10)]"></i>
                </a>
            `
        }
        results.length > 0 ? admin_search_result.innerHTML = rescontent : admin_search_result.innerHTML = `<div class="mt-1 mx-3">نتیجه ای پیدا نشد!</div>`
    }
}


let order_table_partial = document.getElementById('order-table-partial')
//جستجو در رکورد های جدول
let search_tables = (search ,table ,url ,name) => {
    let table_partial = document.getElementById(table)
    let search_value = document.getElementById(search)

    clearTimeout(search_timeout);

    if (controller) {
        controller.abort();
    }
    controller = new AbortController();

    loader.style = 'display: block'
    search_timeout = setTimeout(() => {
        let q = search_value.value.trim()
        fetch(url + `?q=${q}&c=${name ? name : '0'}` ,{signal: controller.signal}).then(res => res.json()).then(
            data => {
                data.data_length > 0 ? table_partial.innerHTML = data.html : table_partial.innerHTML = `<div class="mt-5 text-center w-[100%] mb-3">رکوردی یافت نشد!</div>`
            }
        ).finally(() => {
            name ? ToolbarCheck(name) : null
            loader.style = 'display: none'
        })
    } ,700)
}
//نوار تنظیمات
let ToolbarCheck = (name) => {
    let checks = document.querySelectorAll(`input[name='${name}']`)
    let toolbar = document.getElementById('table-toolbar')
    let toolbar_item = document.getElementById('table-toolbar-item')
    checks.forEach(item => {
        item.addEventListener('change' ,()=> {
            let checks_checked = document.querySelectorAll(`input[name='${name}']:checked`)
            if (checks_checked.length > 0) {
                toolbar.classList.remove('disabled')
                toolbar_item.classList.remove('hidden')
                toolbar_item.innerHTML = `آیتم (${to_fanum(checks_checked.length)})`
            }
            else {
                toolbar.classList.add('disabled')
                toolbar_item.classList.add('hidden')
            }
        })
    })
}
// غیرفعال کردن نوار تنظیمات
let ToolbarDisable = (name)=> {
    let checks = document.querySelectorAll(`input[name="${name}"]`)
    let toolbar = document.getElementById('table-toolbar')
    let toolbar_item = document.getElementById('table-toolbar-item')
    checks.forEach(item => {
        item.checked = false
        toolbar.classList.add('disabled')
        toolbar_item.classList.add('hidden')
    })
}

//اکشن روی سفارشات انتخاب شده
let OrderSelectedAction = (action) => {
    const form = document.getElementById("form-order");
    const data = new FormData(form);
    fetch(`/adminpanel/orders/action/?action=${action}` ,{method: "POST" ,body: data , headers: {"X-CSRFToken": data.get("csrfmiddlewaretoken")}}).then(res => res.json()).then(data => {
        data.message ? Message(data.message ,false) : null
        data.html ? order_table_partial.innerHTML = data.html : null
        ToolbarDisable('order')
        ToolbarCheck('order')
    })
}
//اکشن روی کالا های انتخاب شده
let product_table_partial = document.getElementById('product-table-partial')
let ProductSelectedAction = (action) => {
    const form = document.getElementById("form-product");
    const data = new FormData(form);
    fetch(`/adminpanel/products/action/?action=${action}` ,{method: "POST" ,body: data , headers: {"X-CSRFToken": data.get("csrfmiddlewaretoken")}}).then(res => res.json()).then(data => {
        data.message ? Message(data.message ,false) : null
        data.html ? product_table_partial.innerHTML = data.html : null
        ToolbarDisable('order')
        ToolbarCheck('order')
    })
}

//سورت کردن محصولات
let product_select_sort = document.getElementById('product-select-sort')
let ProductsSort = () => {
    let sort_type = product_select_sort.value
    document.getElementById('loader').style = 'display: block'
    fetch(`/adminpanel/products/?sort=${sort_type}`).then(res => res.json()).then(data => {
        data.data_length > 0 ? product_table_partial.innerHTML = data.html : product_table_partial.innerHTML = `<div class="mt-5 text-center w-[100%] mb-3">رکوردی یافت نشد!</div>`
    }).finally(()=> {
        document.getElementById('loader').style = 'display: none'
    })
}

let article_table_partial = document.getElementById('article-table-partial')
let article_select_sort = document.getElementById('article-select-sort')
let ArticlesSort = () => {
    let sort_type = article_select_sort.value
    document.getElementById('loader').style = 'display: block'
    fetch(`/adminpanel/articles/?sort=${sort_type}`).then(res => res.json()).then(data => {
        data.data_length > 0 ? article_table_partial.innerHTML = data.html : article_table_partial.innerHTML = `<div class="mt-5 text-center w-[100%] mb-3">رکوردی یافت نشد!</div>`
    }).finally(()=> {
        document.getElementById('loader').style = 'display: none'
    })
}

//تایید کامنت توسط مدیر
let comments_approved_partial = document.getElementById('comments-approved-partial')
let comments_notapproved_partial = document.getElementById('comments-notapproved-partial')
let ApproveComment = (comment_pk) => {
    let com_pk = comment_pk
    Showloader(1000)
    fetch(`/adminpanel/comments/?comment=${com_pk}`).then(res => res.json()).then(data => {
        comments_approved_partial.innerHTML = data.html_a
        comments_notapproved_partial.innerHTML = data.html_na
    })
}

let sales_chart_partial = document.getElementById('sales-chart-partial')
let sales_option = document.getElementById('sales-select')
let SalesChartDataChange = () => {
    document.getElementById('loader').style = 'display: block;'
    let sales_data = sales_option.value
    fetch(`/adminpanel/stats/sales-stats/change/?period=${sales_data}`).then(res => res.json()).then(data => {
        sales_chart_partial.innerHTML = data.html
    }).finally(()=> {
        document.getElementById('loader').style = 'display: none'
    })
}


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
        disableOnInteraction: true,
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
            slidesPerView: 2.1
        },
        1800: {
            slidesPerView: 3.5
        }
    }

})


let Product_To_Carousel = (action) => {
    const menu = document.getElementById('carousel-product-menu')
    if (action === true) {
        menu.classList.replace('hidden' ,'centerbox')
        document.getElementById('product-search').focus()
    }
    else {
        menu.classList.replace('centerbox' ,'hidden')
    }
}

let carousel_partial= document.getElementById('carousel-partial')
let Carousel_grab_item = (carousel_pk ,product_pk ,action) => {
    loader.style = 'display:block;'
    fetch(`/adminpanel/carousels/${carousel_pk}/edit/?pk=${product_pk}&action=${action}`).then(res => res.json()).then(data => {
        carousel_partial.innerHTML = data.html
        special_carousel.update()
        special_carousel.updateSize();
        special_carousel.updateSlides();
        special_carousel.updateProgress();
        special_carousel.slideTo(special_carousel.slides.length - 1);
    }).finally(() => {
        loader.style = 'display: none;'
        Product_To_Carousel(false)
    })
}

