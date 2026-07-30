// let $ = document


let btnShowPass = $.getElementById('btn-showpass')
let btnHidePass = $.getElementById('btn-hidepass')
let PasswordLetter = (action ,element) => {
    let input = $.getElementById(element)
    if (action === "show") {
        input.setAttribute('type' ,'text')
        btnShowPass.style = "display: none;"
        btnHidePass.style = "display: block;"
    } 
    else {
        input.setAttribute('type' ,'password')
        btnShowPass.style = "display: block;"
        btnHidePass.style = "display: none;"
    }
}


let PlaceHolderHandle = (inp ,pl ,action) => {
    let inputText = $.getElementById(inp).value
    let plc = $.getElementById(pl)

    if (action === "bl") {
        if (inputText.length > 0) {
            plc.style = "transform: translateY(-25px);"
        }
        else {
            plc.style = "transform: none;"
        }
    }
    else if (action === "fc") {
        plc.style = "transform: translateY(-25px);"
    }
}


let MaxLengthIndicator = (element ,num) => {
    let el = $.getElementById(element)
    if (el.value.length > num) {
        el.value = el.value.slice(0, num)
    }
}



let AccountError = (element ,error ,action) => {
    let el = $.getElementById(element)
    let el_text = $.getElementById(element +"text")
    if (action === "show") {
        el_text.innerHTML = error
        el.style = "display: flex; color: var(--color5)"
    } else {
        el.style = "display: none;"
    }
}



let CheckLogin = (btn ,checkPhone ,checkPass) => {
    let btnLogin = $.getElementById(btn)

    if (checkPhone && checkPass) {
        btnLogin.className = "btn-defIconFlex w-[100%] justify-center gap-1"
        btnLogin.setAttribute('type' ,'submit')
    } else {
        btnLogin.className = "btn-defIconFlex disabled w-[100%] justify-center gap-1"
        btnLogin.setAttribute('type' ,'button')
    }
}

let CheckForgot = (btn ,check) => {
    let btnLogin = $.getElementById(btn)

    if (check) {
        btnLogin.className = "btn-defIconFlex m-1.5"
        btnLogin.setAttribute('type' ,'submit')
    } else {
        btnLogin.className = "btn-defIconFlex m-1.5 disabled"
        btnLogin.setAttribute('type' ,'button')
    }
}

let CheckVer = (btn ,check) => {
    let btnLogin = $.getElementById(btn)

    if (check) {
        btnLogin.className = "btn-defIconFlex w-[100%] justify-center gap-1"
        btnLogin.setAttribute('type' ,'submit')
    } else {
        btnLogin.className = "btn-defIconFlex disabled w-[100%] justify-center gap-1"
        btnLogin.setAttribute('type' ,'button')
    }
}

let PasswordMatch = (pass ,conpass) => {
    let password = $.getElementById(pass).value
    let confirm = $.getElementById(conpass).value
    if (password === confirm) {
        return true
    }
    else {
        return false
    }
}


let IsChecked = false
let IsPassChecked = false
let Checkfield = (element ,type ,err) => {
    let ele = $.getElementById(element)
    let input = ele.value
    const phonePattern = /^09[0-9]{9}$/;
    if (type === "phone" || type === "phone-forgot") {
        if (input.length < 11 || input.length > 11) {
            AccountError(err ,"شماره تلفن باید 11 رقم باشد." ,"show")
            IsChecked = false
            type === "phone-forgot" ? CheckForgot('btn-code' ,IsChecked):null
        }
        else if (input.length === 11) {
            let isPhoneCorrect = phonePattern.test(input)
            if (!isPhoneCorrect) {
                AccountError(err ,"فرمت شماره تلفن اشتباه است!   مثال: 09111234567" ,"show")
                IsChecked = false
                type === "phone-forgot" ? CheckForgot('btn-code' ,IsChecked):null
            }
            else {
                AccountError(err ,null ,"hide")
                IsChecked = true
                type === "phone-forgot" ? CheckForgot('btn-code' ,IsChecked):null
            }
        }
        else {
            AccountError(err ,null ,"hide")
            IsChecked = true                
            type === "phone-forgot" ? CheckForgot('btn-code' ,IsChecked):null
        }
        CheckLogin( 'btn-login' ,IsChecked ,IsPassChecked)
    }
    if (type === "pass") {
        if (input.length < 8) {
            AccountError(err ,"پسورد دارای حداقل 8 کارکتر است" ,"show")
            IsPassChecked = false
        }
        else {
            AccountError(err ,"" ,"hide")
            IsPassChecked = true
        }
    }
    if (type === "conpass") {
        if (input.length >= 8) {
            if (!PasswordMatch(element ,'conpass')) {
                AccountError(err ,"پسورد ها مطابقت ندارند!" ,"show")
                IsPassChecked = false
            }
            else {
                AccountError(err ,"" ,"hide")
                IsPassChecked = true
            }
        }
    }
    if (type === "ver") {
        if (input.length < 6) {
            AccountError(err ,"کد تایید شامل 6 رقم است" ,"show")
            IsPassChecked = false
            CheckVer('btn-login' ,IsPassChecked)
        }
        else {
            AccountError(err ,"" ,"hide")
            IsPassChecked = true
            CheckVer('btn-login' ,IsPassChecked)
        }
        MaxLengthIndicator('ver-pass' ,6)
    }
    CheckLogin('btn-login' ,IsChecked ,IsPassChecked)
}

let CheckPhone = (element ,err ,btn) => {
    let btnLogin = $.getElementById(btn)
    const phonePattern = /^(?:\+98|0)?(?:9\d{9}|[1-8]\d{9})$/;
    let input = $.getElementById(element).value
        if (input.length < 11 || input.length > 11) {
            AccountError(err ,"شماره تلفن باید 11 رقم باشد." ,"show")
            !btnLogin.classList.contains('disabled') ? btnLogin.classList.add('disabled') : null
        }
        else if (input.length === 11) {
            let isPhoneCorrect = phonePattern.test(input)
            if (!isPhoneCorrect) {
                AccountError(err ,"فرمت شماره تلفن اشتباه است!" ,"show")
                !btnLogin.classList.contains('disabled') ? btnLogin.classList.add('disabled') : null
            }
            else {
                AccountError(err ,null ,"hide")
                btnLogin.classList.remove('disabled')
            }
        }
}