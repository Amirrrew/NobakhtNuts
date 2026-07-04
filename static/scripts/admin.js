
let sidebar = document.querySelector('.sidebar-admin')
// نمایش دکمه اسکرول تو تاپ سایدبار
sidebar.addEventListener('scroll' ,()=> {
    if (sidebar.scrollTop > 20) {
        document.getElementById('sidebar-backtotop').style = 'bottom: 10px;'
    } else {document.getElementById('sidebar-backtotop').style = 'bottom: -200px'}
})

// لیست گزینه های پنل ادمین
const admin_options = [
    {title: 'خانه' ,url: '/adminpanel/'},
    {title: 'آمار فروش' ,url: '/adminpanel/'},
    {title: 'سفارشات' ,url: '/adminpanel/'},
    {title: 'محصولات' ,url: '/adminpanel/'},
    {title: 'افزودن محصول جدید' ,url: '/adminpanel/'},
    {title: 'شاخه های اصلی' ,url: '/adminpanel/'},
    {title: 'افزودن شاخه اصلی' ,url: '/adminpanel/'},
    {title: 'زیر شاخه ها' ,url: '/adminpanel/'},
    {title: 'افزودن زیر شاخه' ,url: '/adminpanel/'},
    {title: 'بسته بندی ها' ,url: '/adminpanel/'},
    {title: 'افزودن بسته بندی جدید' ,url: '/adminpanel/'},
    {title: 'برند ها' ,url: '/adminpanel/'},
    {title: 'افزودن برند جدید' ,url: '/adminpanel/'},
    {title: 'کامنت ها' ,url: '/adminpanel/'},
    {title: 'کاربران' ,url: '/adminpanel/'},
    {title: 'افزودن کاربر جدید' ,url: '/adminpanel/'},
    {title: 'مقالات' ,url: '/adminpanel/'},
    {title: 'افزودن مقاله جدید' ,url: '/adminpanel/'},
    {title: 'تیکت های پشتیبانی' ,url: '/adminpanel/'},
    {title: 'راه های ارتباطی' ,url: '/adminpanel/'},
    {title: 'تنظیمات سایت' ,url: '/adminpanel/'},
    {title: 'دسته بندی فوتر لینک' ,url: '/adminpanel/'},
    {title: 'افزودن دسته بندی فوتر لینک' ,url: '/adminpanel/'},
    {title: 'فوتر لینک ها' ,url: '/adminpanel/'},
    {title: 'افزودن فوتر لینک' ,url: '/adminpanel/'},
    {title: 'کارت های بانکی من' ,url: '/adminpanel/'},
    {title: 'افزودن کارت بانکی جدید' ,url: '/adminpanel/'},
    {title: 'نرخ و روش های ارسال' ,url: '/adminpanel/'},
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

