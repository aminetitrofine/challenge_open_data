const months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre "]
// const startYear = 2016 // previously declared at script.js

/* adding event on the slider of the month to change */
const dateSlider = document.querySelector("#dateslider")
const sliderValue = document.querySelector("#date .slidervalue")

function updateValue() {
    const month = months[dateSlider.value%12]
    const year = startYear + Math.floor(dateSlider.value/12)
    const date = new String(month + ' ' + year)
    sliderValue.textContent = date
}

function updatePosition() {
    const thumbOffset = Math.floor(0.05 * dateSlider.offsetWidth);
    // width used by the slider 
    const widthAllowed = dateSlider.offsetWidth - thumbOffset
    // width between start of windows and start of slider
    const windowOffset = Math.floor((window.innerWidth - widthAllowed)/2)
    const sliderValue = document.querySelector("#date .slidervalue")
    const sliderRatio = ( dateSlider.value - dateSlider.min)/ (dateSlider.max - dateSlider.min) 
    const absolutePosition = (windowOffset + sliderRatio*widthAllowed)
    sliderValue.style.left = absolutePosition/window.innerWidth*100 + "%";
}

dateSlider.addEventListener("input", () => {
    updatePosition()
    updateValue()
})

window.addEventListener("load", () => {
    updatePosition()
    updateValue() 
})