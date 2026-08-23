let $ = document
// تعریف متغیر های حیاتی
let parentHeader = $.getElementById('header')
let btn_opensearch = document.getElementById('btn-opensearch')
let headerLogobox = $.getElementById('header-logo')
let header = $.querySelector('header')
let headerLogo = $.getElementById('main-logo')
let headtitle = $.getElementById('head-title')
let headersubbox = $.getElementById('header-subbox')
let menu = $.getElementById('menu')
let menuIcon = $.getElementById('menu-icon')
let headerrow = $.getElementById('header-option-row')
let closeMenu = $.getElementById('close-menu-btn')
let searchbox = $.getElementById('searchbox')
let searchInner = $.getElementById('search-box')
let btnCloseSearch = $.getElementById('close-search')
let logo = $.getElementById('main-logo')
let mainmenu = $.getElementById('main-menu')
let searchinput = $.getElementById('search-input')
let hammenu = $.getElementById('ham-menu')
let side_menu = $.getElementById('side-menu')
let catsidemenu = $.getElementById('cat-sidemenu')
let sidesearch = $.getElementById('search-menu')
let searchSuggest = $.getElementById('search-suggest')
let search_input_mobile = document.getElementById('search-input-mobile')
let lastscroll = 0
let headershrunk = false

// گرفتن تمام لینک های همه صفحات برای اجرا لودینگ بار
let GetAllbtns = () => {
    let btns = document.querySelectorAll('a')
    btns.forEach(item => {
        item.addEventListener('click' ,() => {
            Showloader(3000)
        })
    })
}

GetAllbtns()

// نمایش لودر به زمان مشخص
let Showloader = (time) => {
    document.getElementById('loader').style = 'display: block'
    setTimeout(() => {
        document.getElementById('loader').style = 'display: none'
    } ,time)
}

// اجرای placeholder swap برای سرچ صفحات
let StartIntervals = (start) => {
    null
}

// بررسی بودن در صفحه مورد نظر
function isInSection(section) {
  return window.location.pathname.startsWith(`/${section}`);
}

// بک زدن به صفحه قبل با ریدایرکت
let Back = (url) => {
    window.location.href=`${url}`
}

let footer = document.querySelector('footer')

// انیمیشن و شرینک هدر
let HeaderManage = () => {
    if (window.innerWidth > 1300) {
        if (!isInSection('userpanel')){
            if (document.documentElement.scrollTop > 100) {
                parentHeader.style = "height: 60px"
                headerLogo.style = "width: 35px; height: 35px;";
                headerrow.style = "margin-top: -5px; position: absolute;"
                headtitle.style = "display: none;"
                btn_opensearch.style = 'margin-top: -5px;'
                headersubbox.style = "margin-top: -5px"
                headershrunk = true
            } else {
                parentHeader.style = "height: 95px"
                headerLogo.style = "width: 70px; height: 70px;";
                headerrow.style = "margin-top: 10px; position: relative;"
                headtitle.style = "display: block; font-weight: 800;"
                btn_opensearch.style = 'margin-top: 10px;'
                headersubbox.style = "margin-top: 10px"
                headershrunk = false
            }
        }
    }

}




let panel = document.getElementById("submenu-panel");

let ShowSubmenu = (id) =>{
    document.querySelectorAll('.submenu-panel').forEach(item => {
        item.style.display = 'none'
    })
    document.getElementById(`submenu-${id}`).style.display = 'grid'
}
let overlay = document.getElementById('overlay')
let category_menu = document.getElementById('category-menu')
let CategoryMenu = (action) => {
    if (action === true) {
        category_menu.classList.replace('hidden', 'flex')
        document.getElementById('category-arrow').classList.add('transform-[rotate(180deg)]', 'top-[-5px]')
        category_menu.addEventListener('mouseleave', () => {
            category_menu.classList.replace('flex', 'hidden')
            document.getElementById('category-arrow').classList.replace('transform-[rotate(180deg)]', 'transform-[none]')
            document.getElementById('category-arrow').classList.replace('top-[-5px]', 'top-0')
            category_menu.removeEventListener('mouseleave', () => {})
        })
    }else {
        category_menu.classList.replace('flex', 'hidden')
        document.getElementById('category-arrow').classList.replace('transform-[rotate(180deg)]', 'transform-[none]')
        document.getElementById('category-arrow').classList.replace('top-[-5px]', 'top-0')
        category_menu.removeEventListener('mouseleave', () => {})
    }
}

let Search_action = (action) => {
    if (action === true) {
        searchbox.classList.replace('hidden' ,'flex')
        overlay.classList.replace('hidden' ,'flex')
        CategoryMenu(false)
        searchinput.addEventListener('input' ,() => Search(false))
        document.body.style = 'overflow-y: hidden;'
        searchinput.focus()
    } else {
        searchbox.classList.replace('flex' ,'hidden')
        overlay.classList.replace('flex' ,'hidden')
        searchSuggest.style = 'display: none;'
        searchinput.removeEventListener('input' ,() => Search(false))
        HeaderManage()
        document.body.style = 'overflow-y: scroll;'
    }
}

document.addEventListener('keydown' ,(e)=> {
    if ((e.ctrlKey || e.metaKey) && e.code === 'KeyK') {
        e.preventDefault();
        Search_action(true);
    }
    else if (e.code === 'Escape') {
        Search_action(false)
    }
})

// جستجو بین محصولات
let search_timeout;
let controller = null;
let search_resultbox_result = document.getElementById('search-result-box')
let skeleton = document.querySelectorAll('.skeletons');
let search_resultbox = document.getElementById('search-result');
let search_resultbox_mobile = document.getElementById('search-result-mobile');

let Search = (mobile) => {
    searchSuggest.style = 'display: block'

    clearTimeout(search_timeout);

    if (controller) {
        controller.abort();
    }

    controller = new AbortController();

    search_timeout = setTimeout(() => {

        let q = mobile ? search_input_mobile.value : searchinput.value;

        if (!q.trim()) {
            (!mobile ? search_resultbox : search_resultbox_mobile).innerHTML = "";
            return;
        }

        document.getElementById('loader').style.display = 'block';
        skeleton.forEach(item => item.style.display = 'block');

        fetch(`/products/search/?q=${encodeURIComponent(q)}`, {
            signal: controller.signal
        })
        .then(res => res.json())
        .then(data => {
            let search_result = "";
            if (data.data.length > 0) {
                data.data.forEach((product, p) => {
                    search_result += `
                        <a href="${product.url}" class="search-result-card mt-2 pb-2 border-b border-[#dad9d9]" style="animation: load ${(p + 1) * 150}ms; border-radius:0;">
                            <div class="rounded-2xl min-w-15 min-h-15 max-w-15 bg-[var(--color11)] border border-[#dad9d9] overflow-hidden">
                                <img alt="${product.title}" class="w-full h-full" src="${product.image}">
                            </div>

                            <div class="flex w-full">
                                <div class="w-full">
                                    <div class="flex justify-between items-start ">
                                        <div class="search-result-title flex text-start items-start">
                                            ${to_fanum(product.title)}
                                        </div>
                                    </div>

                                    <div class="flex items-start gap-1">

                                        ${
                                            !product.offer
                                            ?
                                            `<div class="text-2xl">${threeDigitsCurrency(product.price)} تومان</div>`
                                            :
                                            `
                                            <div class="text-[var(--color10)] line-through mt-1">
                                                ${threeDigitsCurrency(product.price)} 
                                            </div>

                                            <div class="text-2xl">
                                                ${threeDigitsCurrency(product.final_price)} تومان
                                            </div>

                                            <div class="px-2 py-0.5 text-[var(--color3)] bg-[var(--color5)] h-5 mt-1 text-sm rounded-lg">
                                                ${to_fanum(product.offer)} %
                                            </div>
                                            `
                                        }

                                    </div>
                                </div>
                            </div>
                        </a>
                    `;
                });

                search_resultbox_result.innerHTML = `
                <div style="background-color: rgba(255,255,255,0.76)" class="flex justify-between px-3 w-[96%] rounded-xl pt-2 bg-[rgba(255, 255, 255, 0.75)] h-10 border border-[var(--color11)]">
                    <div>
                        ${to_fanum(data.result_count)} محصول پیدا شد
                    </div>
                     <a href="/products/?q=${encodeURIComponent(q)}">
                         نمایش همه نتایج <i class="fa fa-angle-left mr-1 mt-1"></i>
                     </a>
                 </div>
                `
            } else {

                search_result = `
                    <div class="${!mobile ? 'mt-3' : 'mt-64'} mx-2" style="animation:load .2s;">
                        نتیجه‌ای برای "${q}" پیدا نشد
                    </div>
                `;

                search_resultbox_result.innerHTML = null
            }
            (!mobile ? search_resultbox : search_resultbox_mobile).innerHTML = search_result;
        })
        .catch(err => {
            if (err.name !== "AbortError") {
                console.error(err);
            }
        })
        .finally(() => {
            document.getElementById('loader').style.display = 'none';
            skeleton.forEach(item => item.style.display = 'none');
        });

    }, 500);
}


// ساید بار صفحات
let SideMenu = (action ,element ,type) => {
    let el = document.getElementById(element)
    if (action === "open") {
        el.style = "transform: translateX(0);"
        document.body.style.overflowY = 'hidden'
    }
    else {
        el.style = "transform: translateX(100%);"
        document.body.style.overflowY = 'scroll'
    }

    if (type === 'search' && action === 'open') {
        search_input_mobile.addEventListener('input' ,()=> Search(true))
    } else if (type === 'search' && action === 'close') {
        search_input_mobile.removeEventListener('input' ,()=> Search(true))
    }
}

const dialogClickHandler = (e) => {
    let popup = document.getElementById('dialog')

    if (!popup.contains(e.target)) {
        CloseDialog()
    }
}

// باز کردن مودال بله خیر
let OpenDialog = (dialogtext ,dialogurl) => {
    let parent = document.getElementById('dialog-parent')
    let dialog = document.getElementById('dialog')

    document.getElementById('dialog-text').innerHTML = dialogtext
    document.getElementById('dialog-btn').href = dialogurl

    window.innerWidth > 1130 ? parent.style = 'display: flex; align-items:center;' :parent.style = 'display: flex; align-items:end;'
    document.body.style.overflowY = 'hidden'
    window.innerWidth < 1130 ? dialog.style = 'animation: popup-mobile 300ms': null
    setTimeout(() => {
        document.addEventListener('click', dialogClickHandler)
    }, 200)

}

function CloseDialog() {
    let dialog = document.getElementById('dialog')
    let parent = document.getElementById('dialog-parent')
    window.innerWidth < 1130 ? dialog.style = 'animation: popup-mobile-close 300ms' : dialog.style = 'animation: unload4 200ms'
    setTimeout(()=> {
        parent.style = 'display: none'
        dialog.style = 'animation: load5 300ms;'
        document.body.style.overflowY = 'scroll'
        document.removeEventListener('click', dialogClickHandler)
    } ,100)
}


// ست کردن عکس روی اینپوت آپلود عکس ها
let SetUploadedImage = (event, parentElement) => {
    var parent = document.getElementById(`${parentElement}`)
    var file = event.target.files[0]

    if (file && file.type.startsWith('image/')) {
        var reader = new FileReader()
        reader.onload = (e) => {
            parent.style.backgroundImage = `url(${e.target.result})`
            parent.style.backgroundSize = 'cover'
        }
        reader.readAsDataURL(file)
    }
    else {
        Message('فقط عکس مجاز است!', true)
        event.target.value = ''
    }
}

let SetUploadedImageSlider = (event, parentElement ,slider) => {
    var parent = document.getElementById(`${parentElement}`)
    var file = event.target.files[0]
    var slide = document.getElementById(slider)
    var icon = document.getElementById('preview-icon')

    if (file && file.type.startsWith('image/')) {
        var reader = new FileReader()
        reader.onload = (e) => {
            parent.style.backgroundImage = `url(${e.target.result})`
            parent.style.backgroundSize = 'cover'
            slide.src = e.target.result
            icon.classList.add('hidden')
        }
        reader.readAsDataURL(file)
    } else {
        Message('فقط عکس مجاز است!', true)
        event.target.value = ''
    }
}

htmladdress = `
    
`

// پاپ آپ اسکرین
let PopUp = (type ,action) => {
    let parent = document.getElementById('popup-parent-pop')
    let popup = document.getElementById('popup-form')

    if (action === 'open') {
        window.innerWidth < 1130 ? parent.style = 'display: flex;' : parent.style = 'display: flex; align-items:center;'
        document.body.style.overflowY = 'hidden'
    } else {
        popup.style = 'animation: unload4 200ms'
        setTimeout(()=> {
            parent.style = 'display: none'
            popup.style = 'animation: load5 300ms;'
            document.body.style.overflowY = 'scroll'
        } ,100)
    }
}

// کپی تکست به کلیپبورد
let CopyToClipboard = (clip_icon ,check_icon ,element) => {
    let clipicon = $.getElementById(clip_icon)
    let checkicon = $.getElementById(check_icon)

    clipicon.style = 'display: none;'
    checkicon.style = 'display: block; animation: load3 500ms; position: relative;'
    navigator.clipboard.writeText(element)
    setTimeout(()=> {
        checkicon.style = 'display: block; animation: unload3 500ms;'
    } ,1500)
    setTimeout(()=> {
        clipicon.style = 'display: block; animation: load2 500ms'
        checkicon.style = 'display: none;'
    } ,2000)
}


// فقط اعداد
function onlyNumbers(element) {
    let el = document.getElementById(element);
    el.value = el.value.replace(/\D/g, '');
}

// جدا کردن سه رقم سه رقم کورنسی
function threeDigitsCurrency(value) {
    return Number(value).toLocaleString('fa-ir');
}

// سواپ با ارقام فارسی
function to_fanum(num) {
  const persianDigits = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];

  return num.toString().replace(/[0-9]/g, (d) => persianDigits[d]);
}

//
function InputSetCurrency(element) {
    let input = document.getElementById(element);
    let value = input.value.replace(/\D/g, "");
    input.value = value.replace(/\B(?=(\d{3})+(?!\d))/g, "،")
}


// تابع باز و بسته کردن دراور (آکاردئون)
let Drawer = (element,drawer ,angle) => {
    let el = $.getElementById(element)
    let draw = $.getElementById(drawer)
    let icon = $.getElementById(angle)

    if (draw.style.display === 'none') {
        el.style = 'height: 400px;'
        draw.style = 'display: block;'
        icon.style = 'transform: rotate(180deg); transition: 200ms; top: -5px'
    }
    else {
        el.style = 'height: 60px;'
        draw.style = 'display: none;'
        icon.style = 'transform: rotate(0); transition: 200ms; top: 0'
    }
}


// آکاردئون سوالات متداول
let DrawerQuestion = (element,drawer ,ic) => {
    let el = $.getElementById(element)
    let draw = $.getElementById(drawer)
    let icon = $.getElementById(ic)

    if (draw.style.display === 'none') {
        el.style = 'height: max-content;'
        draw.style = 'display: block; animation: load5 300ms;'
        icon.style = 'transform: rotate(45deg);'
    }
    else {
        el.style = 'height: auto;'
        draw.style = 'display: none;'
        icon.style = 'transform: rotate(0);'
    }
}


// پیغام
let message_active =false
let Message = (text ,error) => {
    let message = document.getElementById('message')
    let message_time = document.getElementById('message-time')
    let message_text = document.getElementById('message-text')
    let message_icon = document.getElementById('message-icon')
    let message_title = document.getElementById('message-title')

    if (!message_active){
        message_active = true
        if (!error) {
            message_title.innerHTML = 'موفقیت!'
            message_icon.innerHTML = `<svg id="Tick Square" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M12.25 2.78467C5.052 2.78467 2.5 5.33667 2.5 12.5347C2.5 19.7327 5.052 22.2847 12.25 22.2847C19.448 22.2847 22 19.7327 22 12.5347C22 5.33667 19.448 2.78467 12.25 2.78467Z" fill="#674d45"></path><path d="M11.5912 15.4375L16.3412 10.6915C16.6342 10.3985 16.6342 9.92351 16.3412 9.63051C16.0482 9.33851 15.5732 9.33751 15.2802 9.63051L11.0612 13.8465L9.2202 12.0035C8.9282 11.7125 8.4532 11.7105 8.1592 12.0035C7.8662 12.2965 7.8662 12.7715 8.1592 13.0645L10.5302 15.4375C10.6712 15.5785 10.8622 15.6575 11.0612 15.6575C11.2602 15.6575 11.4502 15.5785 11.5912 15.4375Z" fill="#674d45"></path></svg>`
        } else {
            message_title.innerHTML = 'خطا!'
            message_icon.innerHTML = `<svg id="Danger" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M19.3101 10.6927L19.0981 10.3187C16.1121 5.00867 14.2561 3.03467 12.2501 3.03467C10.2441 3.03467 8.38808 5.00867 5.40208 10.3187L5.19108 10.6927C4.11808 12.5747 1.88808 16.4897 2.30208 18.8257C2.79008 21.5887 5.63508 22.0347 12.2501 22.0347C18.8661 22.0347 21.7111 21.5887 22.1981 18.8257C22.6121 16.4897 20.3821 12.5747 19.3101 10.6927Z" fill="#674d45"></path><path d="M11.5005 16.4297C11.5005 16.8437 11.8405 17.1797 12.2545 17.1797C12.6685 17.1797 13.0045 16.8437 13.0045 16.4297C13.0045 16.0157 12.6685 15.6797 12.2545 15.6797H12.2455C11.8315 15.6797 11.5005 16.0157 11.5005 16.4297Z" fill="#674d45"></path><path d="M12.2495 8.28467C11.8355 8.28467 11.4995 8.62067 11.4995 9.03467V12.9297C11.4995 13.3437 11.8355 13.6797 12.2495 13.6797C12.6635 13.6797 12.9995 13.3437 12.9995 12.9297V9.03467C12.9995 8.62067 12.6635 8.28467 12.2495 8.28467Z" fill="#674d45"></path></svg>`
        }

        message_time.style.animation = "ShowmessageTime 4s"
        if (window.innerWidth > 1130) {
            !error ? message.style.animation = "Showmessage_desktop 4s" : message.style.animation = "Showmessage-e-desktop 4s";
        }
        else {
            !error ? message.style.animation = "Showmessage_mobile 4s" : message.style.animation = "Showmessage-e-mobile 4s";
        }
        message_text.innerHTML = text

        setTimeout(() => {
            message_time.style.animation = "none"
            message.style.animation = "none"
            message_active = false
        } ,4000)
    }
}

// بستن پیغام
let CloseMessage = () => {
    let message = document.getElementById('message')
    let message_time = document.getElementById('message-time')
    let message_text = document.getElementById('message-text')
    let message_icon = document.getElementById('message-icon')
    clearTimeout(Message)
    message_time.style.animation = "none"
    message.style.animation = "none"
    message_active = false
}


// اعمال قیمت روی بسته بندی محصول با توجه به وزن
let CartCheck = (id ,productprice ,size ,packtitle) => {
    let btn = document.getElementById(id)
    let pricebox = document.querySelectorAll('.pricebox')
    let price = productprice
    if (btn)
        btn.style = 'pointer-events: all; background-color: var(--color6); height: 50px; padding-top: 13px;'
    pricebox.forEach(item => {item.style = 'background-color: var(--color19); border: 2px solid var(--color16); display: flex; animation: load5 300ms; justify-content: space-between; margin-top: 10px; margin-bottom: 2px;'})

    setTimeout(()=> {
        pricebox.style = 'display: flex; animation: none;'
    },300)

    let cartpackhtml = `
    <div class="text-[var(--color10)] text-thin mt-1.5">قیمت بسته ${to_fanum(packtitle)}</div>
    <div class="text-black mt-0.5 text-3xl font-semibold">${threeDigitsCurrency(price * size)} تومان</div>
    `
    pricebox.forEach(item => {item.innerHTML = cartpackhtml})
}

// دریافت پک های انتخاب شده محصول
function getSelectedPack() {
    return document.querySelector('input[name="pack_mobile"]:checked')
        || document.querySelector('input[name="pack"]:checked');
}

// افزودن به سبد خرید
let AddToOrder = (productId ,isWeight ,pack_id) => {
    let pack = getSelectedPack()
    let btnAddtocart = document.getElementById('btn-addtocart')
    let url = null;

    if (isWeight === 'false') {
        url = `/orders/add-to-order/?product_id=${productId}`;
    } else {
        if (pack_id) {
            url = `/orders/add-to-order/?product_id=${productId}&pack_id=${pack_id}`;
        } else {
            url = `/orders/add-to-order/?product_id=${productId}&pack_id=${pack.value}`;
        }
    }

    document.getElementById('loader').style = 'display: block;'
    if (pack_id) {
        document.getElementById('pack-weights').classList.add('disabled')
    }
    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                data.error ? Message(data.message ,true) : Message(data.message ,false);
            }
            btnAddtocart.style = 'pointer-events: none; background-color: var(--color9); height: 50px; padding-top: 13px;'
            if (data.html) {
                document.querySelectorAll('.cart-items').forEach(item => {
                    item.innerHTML = data.html;
                });
                PrdNav(true)
            }
        }).catch(err => {
            Message('افزودن به سبد خرید با خطا مواجه شد' ,true)
    }).finally(()=> {
            document.getElementById('pack-weights').classList.remove('disabled')
            if (pack_id) {
                PopUpWeight('none' ,'close')
            }
            document.getElementById('loader').style = 'display: none;'
            btnAddtocart.style = 'pointer-events: all; background-color: var(--color6); height: 50px; padding-top: 13px;'
        })
}

// تغییر مقدار آیتم سبد خرید
let change_order_count = (detail_id ,type ,page ,pack) => {
    let url = ''
    if (pack) {
        url = `/orders/change-order-count/?detail_id=${detail_id}&type=${type}&page=${page}&pack=${pack}`
    } else {
        url = `/orders/change-order-count/?detail_id=${detail_id}&type=${type}&page=${page}`
    }
    document.getElementById('loader').style = 'display: block;'
    fetch(url).then(res => res.json()).then(data => {
        if (data.message) {
            data.error ? Message(data.message ,true) : Message(data.message ,false);
        }
        if (data.html) {
            document.querySelectorAll('.cart-items').forEach(item => {
                item.innerHTML = data.html;
            });
        }
    }).catch(err => {
            Message('بروزرسانی سبد با خطا مواجه شد', true)
        }).finally(()=> {
        document.getElementById('loader').style = 'display: none;'
    })
}

// منوی نویگیشن و قیمت محصول موبایل
let navopen = true
let PrdNav = (force) => {
    let btnnav = document.getElementById('btn-navicon')
    let prditems = document.getElementById('prd-items-mobile')

    if (force) {
        prditems.style = 'display: block; animation: load 300ms;'
        btnnav.style = 'transform: none'
        navopen = true
    }
    else {
        if (navopen) {
            prditems.style = 'display: none'
            btnnav.style = 'transform: rotate(180deg)'
            navopen = false
        }
        else {
            prditems.style = 'display: block; animation: load 300ms;'
            btnnav.style = 'transform: none'
            navopen = true
        }
    }
}

// لایک کردن کامنت
function LikeAction(id) {
    document.getElementById('loader').style = 'display: block;'
    fetch(`/products/likecomment/?id=${id}`)
        .then(res => res.json())
        .then(data => {

            if (data.message) {
                Message(data.message, data.error);
            }

        if (data.html) {
            document.querySelectorAll('.comments').forEach(item => {
                item.innerHTML = data.html;
            });
        }
        }).finally(()=> {
        document.getElementById('loader').style = 'display: none;'
        })
}


// امتیاز دهی برای کامنت


// اسکرول به میزان مشخص
let ScrollTo = (element) => {
    let section = document.getElementById(element)
    section ? document.documentElement.scrollTop = section.offsetTop - 100 : null
}

// نویگیشن پرداخت موبایل
let payopen = true
let PayNav = (force) => {
    let btnnav = document.getElementById('btn-navicon')
    let prditems = document.querySelectorAll('.payment-item')

    if (force) {
        prditems.forEach(item => {item.style = 'display: block; animation: load 300ms;'})
        btnnav.style = 'transform: none'
        payopen = true
    }
    else {
        if (payopen) {
            prditems.forEach(item => {item.style = 'display: none'})
            btnnav.style = 'transform: rotate(180deg)'
            payopen = false
        }
        else {
            prditems.forEach(item => {item.style = 'display: block; animation: load 300ms;'})
            btnnav.style = 'transform: none'
            payopen = true
        }
    }
}

let inventory_partial = document.getElementById('basket-inventory-partial')
let inventory_content = document.getElementById('inventory-content')
let Get_orderdetail_packs = (detail_id) => {
    let inventory_partial = document.getElementById('basket-inventory-partial')
    loader.style = 'display: block'
    document.getElementById('skeletons-order').classList.replace('hidden' ,'block')
    document.getElementById('inventory-content').style.display = 'none';

    fetch(`/orders/change-order-count/?type=get&detail_id=${detail_id}&page=basket`).then(res => res.json()).then(data => {
        if (data.html) {
            inventory_partial.innerHTML = data.html
        } else {
            Message('در دریافت اطلاعات مشکلی پیش آمده!' ,true)
        }
    }).catch(err => {
            Message('دریافت اطلاعات با خطا مواجه شد' ,true)
    }).finally(()=> {
        loader.style = 'display: none;'
        let content = document.getElementById('inventory-content')
        if (content) content.style.display = 'block'
        document.getElementById('skeletons-order').classList.replace('block' ,'hidden')
    })
}

const popupClickHandler = (e) => {
    let popup = document.getElementById('popup-form')

    if (!popup.contains(e.target)) {
        PopUpOrder('none', 'close')
    }
}

let PopUpOrder = (type ,action) => {
    let parent = document.getElementById('popup-parent-pop')
    let popup = document.getElementById('popup-form')

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


let payment_totalbox_partial_desktop = document.getElementById('payment-totalbox-partial-desktop')
let payment_totalbox_partial_mobile = document.getElementById('payment-totalbox-partial-mobile')

let ApplyDiscount = () => {
    let code_input = document.getElementById('code-input')
    let btn_d = document.getElementById('btn-discount')
    let error = document.getElementById('code-err')
    let error_text = document.getElementById('code-errtext')
    let code = code_input.value.trim()
    let page;
    if (window.innerWidth > 1000) {
        page = 'desktop'
    } else {
        page = 'mobile'
    }
    if (code.length > 5) {
        loader.style = 'display: block;'
        btn_d.classList.add('disabled')
        code_input.classList.add('disabled')
        fetch(`/orders/apply-code/?d=${code}&page=${page}`).then(res => res.json()).then(data => {
            if (data.error) {
                error.style = "display: flex; color: var(--color5)"
                error_text.innerHTML = data.message
            } else {
                Message(data.message, false)
                PopUpOrder('none', 'close')
                page === 'desktop' ? payment_totalbox_partial_desktop.innerHTML = data.html : payment_totalbox_partial_mobile.innerHTML = data.html
            }
        }).catch(err => {
            Message('اعمال کد تخفیف با خطا مواجه شد' ,true)
        }).finally(() => {
            loader.style = 'display: none;'
            btn_d.classList.remove('disabled')
            code_input.classList.remove('disabled')
        })
    } else {
        error.style = "display: flex; color: var(--color5)"
        error_text.innerHTML = 'کد تخفیف را به درستی وارد کنید'
    }
}


let deferredPrompt = null;

const installBtn = document.getElementById('install-app-btn');
let spinner = document.getElementById('spinner')
if (installBtn) {
    spinner.style.display = 'block'
    installBtn.style.display = 'none'
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        installBtn.style.display = 'flex';
        spinner.style.display = 'none'
    });

    installBtn.addEventListener('click', async () => {
        if (!deferredPrompt) {
            return;
        }
        deferredPrompt.prompt();
        const {outcome} = await deferredPrompt.userChoice;
        console.log('Install result:', outcome);
        deferredPrompt = null;
        installBtn.style.display = 'none';
        spinner.style.display = 'none'

    });
}

const popupClickHandlerWeight = (e) => {
    let popup = document.getElementById('popup-form-weight')

    if (!popup.contains(e.target)) {
        PopUpWeight('none', 'close')
    }
}

let PopUpWeight = (type ,action) => {
    let parent = document.getElementById('popup-parent-weight')
    let popup = document.getElementById('popup-form-weight')

        if (action === 'open') {
            window.innerWidth > 1130 ? parent.style = 'display: flex; align-items:center;' :parent.style = 'display: flex; align-items:end;'
            document.body.style.overflowY = 'hidden'
            window.innerWidth < 1130 ? popup.style = 'animation: popup-mobile 300ms': null
            setTimeout(() => {
                document.addEventListener('click', popupClickHandlerWeight)
            }, 200)
        } else {
            window.innerWidth < 1130 ? popup.style = 'animation: popup-mobile-close 300ms' : popup.style = 'animation: unload4 200ms'
            setTimeout(()=> {
                parent.style = 'display: none'
                popup.style = 'animation: load5 300ms;'
                document.body.style.overflowY = 'scroll'
                document.removeEventListener('click', popupClickHandlerWeight)
            } ,100)
        }
}

const ratings_emotion = [
    {title: '1 / 5' ,emoji: '😡'},
    {title: '2 / 5' ,emoji: '☹️'},
    {title: '3 / 5' ,emoji: '😐'},
    {title: '4 / 5' ,emoji: '🙂'},
    {title: '5 / 5' ,emoji: '😀'},
]


let is_rated = false
let is_comment_written = false
let SetRating = (rate) => {
    let rating_input = document.getElementById('final-rating')
    let your_rating = document.getElementById('comment-your-rating')
    rating_input.value = rate
    for (let i = 1; i<= 5; i++) {
        let star = document.querySelector(`.star-${i}`)
        if (i <= rate) {
            star.classList.remove('text-[var(--color14)]')
            star.classList.add('text-[var(--color6)]')
        } else {
            star.classList.remove('text-[var(--color6)]')
            star.classList.add('text-[var(--color14)]')
        }
    }
    document.getElementById('comment-rating').innerHTML = to_fanum(ratings_emotion[rate -1].title)
    document.getElementById('comment-emotion').innerHTML = ratings_emotion[rate-1].emoji
    your_rating.classList.replace('hidden' ,'flex')
    document.getElementById('comment-tip').classList.add('hidden')
    is_rated = true
    CheckCommentCondition()
}

let CheckCommentCondition = () => {
    let comment_text = document.getElementById('comment-inp')
    if (comment_text.value.length > 0) {
        is_comment_written = true
    } else {
        is_comment_written = false
    }
    if (is_rated && is_comment_written) {
        document.getElementById('btn-sendcomment').classList.remove('disabled')
    } else {
        is_comment_written = false
        document.getElementById('btn-sendcomment').classList.add('disabled')
    }
}

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