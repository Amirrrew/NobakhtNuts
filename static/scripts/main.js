let $ = document
// تعریف متغیر های حیاتی
let parentHeader = $.getElementById('header')
let headerLogobox = $.getElementById('header-logo')
let header = $.getElementById('header-box')
let headerLogo = $.getElementById('main-logo')
let headtitle = $.getElementById('head-title')
let headersubbox = $.getElementById('header-subbox')
let menu = $.getElementById('menu')
let menuIcon = $.getElementById('menu-icon')
let headerrow = $.getElementById('header-option-row')
let closeMenu = $.getElementById('close-menu-btn')
let searchbox = $.getElementById('header-search')
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
    start ? setInterval(() => {
        searchinput.setAttribute('placeholder', `مثلا...  ${PlaceHolderText()}`)
    }, 3000) : null
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
                searchbox.style = "margin-top: -5px;"
                headersubbox.style = "margin-top: -5px"
                headershrunk = true
            } else {
                parentHeader.style = "height: 95px"
                headerLogo.style = "width: 70px; height: 70px;";
                headerrow.style = "margin-top: 10px; position: relative;"
                headtitle.style = "display: block; font-weight: 800;"
                searchbox.style = "margin-top: 10px;"
                headersubbox.style = "margin-top: 10px"
                headershrunk = false
            }
        }
    }
}


// باز بسته کردن منوی تاپ و دسته بندی و سرچ
let menuopen = false
let searchopen = false
let Menu = (model, searchManage) => {
    if (model === "cat" && menuopen === false && searchopen === false) {
        parentHeader.style = 'height: 100%;'
        header.style = 'height: 100%;'
        menu.style = "opacity: 1; display: flex;"
        headerrow.style = 'animation: unload 200ms; display: none;'
        closeMenu.style = "display: flex; animation: load 200ms;"
        headerLogobox.style = "animation: unload2 300ms; display: none;"
        document.body.style.overflowY = 'hidden'
        menuopen = true
    }
    else if (model === "cat" && menuopen === true && searchopen === false) {
        parentHeader.style = 'height: 95px;'
        header.style = 'height: 95px;'
        menu.style = "opacity: 0; display: none;"
        headerrow.style = 'animation: load2 200ms; display: flex; margin-top: 10px'
        closeMenu.style = "display: none; animation: unload 200ms;"
        headerLogobox.style = "animation: load 300ms; opacity:1; display: flex;"
        document.body.style.overflowY = 'scroll'
        menuopen = false
        HeaderManage()
    }
    else if (searchManage === 'open' && model === "search" && menuopen === false && searchopen === false) {
        searchbox.style = "animation: OpenSearch 400ms; position: fixed; width: 97%; top: 80px; height: 60px; right: 20px; margin-top: 10px;"
        searchInner.style = 'gap: 10px'
        parentHeader.style = 'height: 100%;'
        header.style = 'height: 100%;'
        searchSuggest.style = "opacity: 1; display: block;"
        headerrow.style = 'animation: unload 200ms; display: none;'
        btnCloseSearch.style = 'display: block;'
        document.body.style.overflowY = 'hidden'
        searchopen = true
        searchinput.addEventListener('input' ,() => Search(false))
    }
    else if (searchManage === 'close' && model === "search" && menuopen === false && searchopen === true) {
        searchbox.style = "animation: CloseSearch 400ms; position: relative; width: 300px; top: 0px; height: 50px; marin-top: 0;"
        searchInner.style = "gap: 0;"
        parentHeader.style = 'height: 130px;'
        header.style = 'height: 130px;'
        searchSuggest.style = "opacity: 0; display: none;"
        headerrow.style = 'animation: load2 200ms; display: flex;'
        btnCloseSearch.style = 'display: none;'
        document.body.style.overflowY = 'scroll'
        searchopen = false
        HeaderManage()
        searchinput.removeEventListener('input' ,() => Search(false))
    }
}

// جستجو بین محصولات
let search_timeout;
let controller = null;

let skeleton = document.querySelectorAll('.skeletons');
let search_resultbox = document.getElementById('search-result');
let search_resultbox_mobile = document.getElementById('search-result-mobile');

let Search = (mobile) => {

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
            if (data.length > 0) {
                data.forEach((product, p) => {
                    search_result += `
                        <a href="${product.url}" class="search-result-card mt-2 pb-2 border-b border-[var(--color16)]" style="animation: load ${(p + 1) * 150}ms; border-radius:0;">
                            <div class="rounded-2xl min-w-20 min-h-20 max-w-20 bg-[var(--color15)] overflow-hidden">
                                <img class="w-full h-full" src="${product.image}">
                            </div>

                            <div class="flex w-full">
                                <div class="w-full">
                                    <div class="flex justify-between items-start mt-2">
                                        <div class="search-result-title flex text-start text-2xl items-start">
                                            ${to_fanum(product.title)}
                                            <div class="bg-[var(--color12)] px-1.5 py-1 text-sm mr-2 rounded-lg">
                                                ${product.is_byWeight ? 'کیلویی' : 'عددی'}
                                            </div>
                                        </div>

                                        <div class="bg-[var(--color12)] text-[var(--color6)] text-center centerbox gap-1 py-0.5 px-2 rounded-xl">
                                            <i class="fa fa-star text-xs mt-1"></i>
                                            ${to_fanum(product.rating)}
                                        </div>
                                    </div>

                                    <div class="flex items-start gap-1">

                                        ${
                                            !product.offer
                                            ?
                                            `<div class="text-2xl">${threeDigitsCurrency(product.price)} تومان</div>`
                                            :
                                            `
                                            <div class="text-sm text-[var(--color10)] line-through mt-1">
                                                ${threeDigitsCurrency(product.price)} تومان
                                            </div>

                                            <div class="text-2xl">
                                                ${threeDigitsCurrency(product.final_price)} تومان
                                            </div>

                                            <div class="px-1 py-0.5 text-[var(--color3)] bg-[var(--color5)] h-6 rounded-lg">
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
            } else {

                search_result = `
                    <div class="${!mobile ? 'mt-20' : 'mt-64'} mx-2" style="animation:load .2s;">
                        نتیجه‌ای برای "${q}" پیدا نشد
                    </div>
                `;
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

// placeholder swap سرچ باکس
let textlist = [
    "پسته احمد آقایی 26 دانه",
    "برنج طارم بوجاری",
    "برگه زردآلو محلی",
    "آلو طرقبه قرمز",
    "بادام درختی شور ایرانی",
    "انجیر استهبان صدیک پرک",
    "زرشک پفکی",
    "بادام زمینی شور آستانه",
    "مویز ازبک درشت"
]

let current_index = 0
let PlaceHolderText = () => {
    let current_text = ''
    if (current_index >= 0 || current_index <= 8) {
        current_text = textlist[current_index]
        if (current_index + 1 !== 9) {
            current_index++
        }
        else {
            current_index = 0
        }
    }

    return current_text
}


// ساید بار صفحات
let SideMenu = (action ,element ,type) => {
    let el = document.getElementById(element)
    if (action === "open") {
        el.style = "right: 0;"
        document.body.style.overflowY = 'hidden'
    }
    else {
        el.style = "right: -100%"
        document.body.style.overflowY = 'scroll'
    }

    if (type === 'search' && action === 'open') {
        search_input_mobile.addEventListener('input' ,()=> Search(true))
    } else if (type === 'search' && action === 'close') {
        search_input_mobile.removeEventListener('input' ,()=> Search(true))
    }
}


// باز کردن مودال بله خیر
let OpenDialog = (dialogtext ,dialogurl) => {
    let dialog = document.getElementById('dialog')
    dialog.style.top = "10px"
    dialog.style.animation = "ShowDialog 3s"

    dialoghtml = `
                <div class="centerbox" style="margin-top: 30px">
                    <div class="">
                        <div class="centerbox">
                            <svg id="Danger" width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M19.3101 10.6927L19.0981 10.3187C16.1121 5.00867 14.2561 3.03467 12.2501 3.03467C10.2441 3.03467 8.38808 5.00867 5.40208 10.3187L5.19108 10.6927C4.11808 12.5747 1.88808 16.4897 2.30208 18.8257C2.79008 21.5887 5.63508 22.0347 12.2501 22.0347C18.8661 22.0347 21.7111 21.5887 22.1981 18.8257C22.6121 16.4897 20.3821 12.5747 19.3101 10.6927Z" fill="#674d45"></path>
                            <path d="M11.5005 16.4297C11.5005 16.8437 11.8405 17.1797 12.2545 17.1797C12.6685 17.1797 13.0045 16.8437 13.0045 16.4297C13.0045 16.0157 12.6685 15.6797 12.2545 15.6797H12.2455C11.8315 15.6797 11.5005 16.0157 11.5005 16.4297Z" fill="#674d45"></path>
                            <path d="M12.2495 8.28467C11.8355 8.28467 11.4995 8.62067 11.4995 9.03467V12.9297C11.4995 13.3437 11.8355 13.6797 12.2495 13.6797C12.6635 13.6797 12.9995 13.3437 12.9995 12.9297V9.03467C12.9995 8.62067 12.6635 8.28467 12.2495 8.28467Z" fill="#674d45"></path>
                            </svg>
                        </div>
                        <div style="margin-top: 20px; color: var(--color6)">
                            ${dialogtext}
                        </div>
                    </div>
                </div>
                <div style="padding: 10px">
                    <div style="display: flex; position:fixed; bottom: 10px; width: 100%; gap: 10px">
                        <a href="${dialogurl}" style="width: 47%"><button class="btn-defIconFlex text-center" style="width: 100%; height: 50px; font-size: 17px; display: block" onclick="CloseDialog()"><i class="fa fa-trash ml-1 text-[var(--color10)]"></i>حذف</button></a>
                        <button id="btn-dialog" class="btn-defIconFlex2" style="width: 45%; height: 50px; border-radius: 10px; display: block" onclick="CloseDialog()">لغو</button>
                    </div>
                </div>
            `

    dialog.innerHTML = dialoghtml
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

htmladdress = `
    
`

// پاپ آپ اسکرین
let PopUp = (type ,action) => {
    let parent = document.getElementById('popup-parent-pop')
    let popup = document.getElementById('popup-form')

    if (action === 'open') {
        parent.style = 'display: flex'
        document.body.style.overflowY = 'hidden'
    } else {
        popup.style = 'animation: unload3 200ms'
        setTimeout(()=> {
            parent.style = 'display: none'
            popup.style = 'animation: load4 500ms;'
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

    if (!message_active){
        message_active = true
        if (!error) {
            message_icon.innerHTML = `<svg id="Tick Square" width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M12.25 2.78467C5.052 2.78467 2.5 5.33667 2.5 12.5347C2.5 19.7327 5.052 22.2847 12.25 22.2847C19.448 22.2847 22 19.7327 22 12.5347C22 5.33667 19.448 2.78467 12.25 2.78467Z" fill="#674d45"></path><path d="M11.5912 15.4375L16.3412 10.6915C16.6342 10.3985 16.6342 9.92351 16.3412 9.63051C16.0482 9.33851 15.5732 9.33751 15.2802 9.63051L11.0612 13.8465L9.2202 12.0035C8.9282 11.7125 8.4532 11.7105 8.1592 12.0035C7.8662 12.2965 7.8662 12.7715 8.1592 13.0645L10.5302 15.4375C10.6712 15.5785 10.8622 15.6575 11.0612 15.6575C11.2602 15.6575 11.4502 15.5785 11.5912 15.4375Z" fill="#674d45"></path></svg>`
        } else {
            message_icon.innerHTML = `<svg id="Danger" width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M19.3101 10.6927L19.0981 10.3187C16.1121 5.00867 14.2561 3.03467 12.2501 3.03467C10.2441 3.03467 8.38808 5.00867 5.40208 10.3187L5.19108 10.6927C4.11808 12.5747 1.88808 16.4897 2.30208 18.8257C2.79008 21.5887 5.63508 22.0347 12.2501 22.0347C18.8661 22.0347 21.7111 21.5887 22.1981 18.8257C22.6121 16.4897 20.3821 12.5747 19.3101 10.6927Z" fill="#674d45"></path><path d="M11.5005 16.4297C11.5005 16.8437 11.8405 17.1797 12.2545 17.1797C12.6685 17.1797 13.0045 16.8437 13.0045 16.4297C13.0045 16.0157 12.6685 15.6797 12.2545 15.6797H12.2455C11.8315 15.6797 11.5005 16.0157 11.5005 16.4297Z" fill="#674d45"></path><path d="M12.2495 8.28467C11.8355 8.28467 11.4995 8.62067 11.4995 9.03467V12.9297C11.4995 13.3437 11.8355 13.6797 12.2495 13.6797C12.6635 13.6797 12.9995 13.3437 12.9995 12.9297V9.03467C12.9995 8.62067 12.6635 8.28467 12.2495 8.28467Z" fill="#674d45"></path></svg>`
        }

        message_time.style.animation = "ShowmessageTime 3s"
        !error ? message.style.animation = "Showmessage 3s" : message.style.animation = "Showmessage-e 3s";
        message_text.innerHTML = text

        setTimeout(() => {
            message_time.style.animation = "none"
            message.style.animation = "none"
            message_active = false
        } ,3000)
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
    let pricebox = document.getElementById('pricebox')
    let price = productprice
    btn.style = 'pointer-events: all; background-color: var(--color6); height: 50px; padding-top: 13px;'
    pricebox.style = 'display: block; animation: load5 300ms;'

    setTimeout(()=> {
        pricebox.style = 'display: block; animation: none;'
    },300)

    let cartpackhtml = `
    <div class="text-[var(--color10)] text-sm text-thin">قیمت بسته ${to_fanum(packtitle)}</div>
    <div class="text-black">${threeDigitsCurrency(price * size)} تومان</div>
    `
    pricebox.innerHTML = cartpackhtml
}

// دریافت پک های انتخاب شده محصول
function getSelectedPack() {
    return document.querySelector('input[name="pack_mobile"]:checked')
        || document.querySelector('input[name="pack"]:checked');
}

// افزودن به سبد خرید
let AddToOrder = (productId, count ,isWeight) => {
    let pack = getSelectedPack()
    let btnAddtocart = document.getElementById('btn-addtocart')
    let url = null;

    if (isWeight === 'false') {
        url = `/orders/add-to-order/?product_id=${productId}&count=${count}`;
    } else {
        url = `/orders/add-to-order/?product_id=${productId}&count=${count}&pack=${pack.value}`;
    }

    document.getElementById('loader').style = 'display: block;'
    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                Message(data.message, data.error);
            }
            btnAddtocart.style = 'pointer-events: none; background-color: var(--color9); height: 50px; padding-top: 13px;'
            if (data.html) {
                document.querySelectorAll('.cart-items').forEach(item => {
                    item.innerHTML = data.html;
                });
                PrdNav(true)
            }
            setTimeout(() => {
                btnAddtocart.style = 'pointer-events: all; background-color: var(--color6); height: 50px; padding-top: 13px;'
            } ,3000)
        }).finally(()=> {
        document.getElementById('loader').style = 'display: none;'
        })
}

// تغییر مقدار آیتم سبد خرید
let change_order_count = (detail_id ,type) => {
    let url = `/orders/change-order-count/?detail_id=${detail_id}&type=${type}`
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
    }).finally(()=> {
        document.getElementById('loader').style = 'display: none;'
        })
}

// تغییر مقدار آیتم سبد خرید (بکست)
let change_order_count_basket = (detail_id, type) => {
    let url = `/orders/change-order-count-basket/?detail_id=${detail_id}&type=${type}`
    document.getElementById('loader').style = 'display: block;'
    fetch(url).then(res => res.json()).then(data => {
        if (data.message) {
            data.error ? Message(data.message, true) : Message(data.message, false);
        }
        if (data.html) {
            document.querySelector('.cart-items-basket').innerHTML = data.html;
        }
    }).finally(()=> {
        document.getElementById('loader').style = 'display: none;'
        })
}

// منوی نویگیشن و قیمت محصول موبایل
let navopen = true
let PrdNav = (force) => {
    let btnnav = document.getElementById('btn-navicon')
    let prditems = document.getElementById('prd-items-mobile')
    let packsize = document.getElementById('prd-packsize')

    if (force) {
        prditems.style = 'display: block; animation: load 300ms;'
        btnnav.style = 'transform: none'
        packsize.style = 'display: block'
        navopen = true
    }
    else {
        if (navopen) {
            prditems.style = 'display: none'
            btnnav.style = 'transform: rotate(180deg)'
            packsize.style = 'display: none'
            navopen = false
        }
        else {
            prditems.style = 'display: block; animation: load 300ms;'
            btnnav.style = 'transform: none'
            packsize.style = 'display: block'
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
const input = document.getElementById("ratingInput");
const front = document.querySelector(".star-front");

const max = 5;

function update_rating() {
  let value = Number(input.value);
  value = Math.max(0, Math.min(max, value));

  const percent = (value / max) * 100;

  front.style.clipPath = `inset(0 ${100 - percent}% 0 0)`;
}


// تغییر ریتینگ
let change_rating = (action) => {
    let input = document.getElementById('ratingInput');
    let star = document.querySelector('.star')
    const max = 5;

    let value = Number(input.value);

    if (action === 'increase') {
        if (value + 1 <= max) {
            value = value + 1;
            star.style = 'animation: posRate 300ms';
            setTimeout(() => {
                star.style = 'aniamtion: none'
            },200)
        }
    } else {
        if (value - 1 >= 1) {
            value = value - 1;
            star.style = 'animation: negRate 300ms';
            setTimeout(() => {
                star.style = 'aniamtion: none'
            },200)
        }
    }

    input.value = value;
    update_rating()
}

// اسکرول به میزان مشخص
let ScrollTo = (element) => {
    let section = document.getElementById(element)
    section ? document.documentElement.scrollTop = section.offsetTop - 100 : null
}

// اعمال هزینه پست
let ApplyPostageFee = (type) => {
    fetch(`/orders/apply-fee/?type=${type}`).then(res => res.json()).then(
        data => {
            if (data.message) {
                Message(data.message, data.error);
            }

            if (data.html) {
                document.querySelectorAll('.checkout').forEach(item => {
                    item.outerHTML = data.html;
                });
            }
        }
    )
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