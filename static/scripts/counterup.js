function SetNumberCounter(elementId, endNumber, options = {}) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.error(`عنصر با آیدی "${elementId}" پیدا نشد`);
        return;
    }

    const duration = options.duration || 1500;
    const startNumber = options.start || 0;
    const useFarsiDigits = options.farsiDigits !== false;

    const farsiDigitsMap = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

    function toFarsiNumber(num) {
        return String(num).replace(/[0-9]/g, (d) => farsiDigitsMap[d]);
    }

    const startTime = performance.now();

    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        const eased = 1 - Math.pow(1 - progress, 3);

        const currentValue = Math.floor(
            startNumber + (endNumber - startNumber) * eased
        );

        element.textContent = useFarsiDigits
            ? toFarsiNumber(currentValue)
            : currentValue;

        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = useFarsiDigits
                ? toFarsiNumber(endNumber)
                : endNumber;
        }
    }

    requestAnimationFrame(updateCounter);
}

function initCounterOnScroll(elementId, endNumber, options = {}) {
    const element = document.getElementById(elementId);
    if (!element) return;

    let started = false;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting && !started) {
                started = true;
                SetNumberCounter(elementId, endNumber, options);
                observer.unobserve(element);
            }
        });
    }, { threshold: 0.3 });

    observer.observe(element);
}
