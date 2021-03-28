"use strict"


function createSVGNode(tagName) {
    return document.createElementNS("http://www.w3.org/2000/svg", tagName)
}

function setNSLinkToElement(element, name) {
    element.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", name)
}


const order = [0, 5, 3, 7, 1, 8, 6, 2, 4]
const animationInterval = 0.1
const animationDuration = 0.7
const durationSum = 5.0

var animationElements = createSVGNode("g")
let transform
let fadeIn
order.forEach((id, index) => {
    transform = createSVGNode("animateTransform")
    setNSLinkToElement(transform, `#ns${id}`)
    transform.setAttribute("attributeType", "XML")
    transform.setAttribute("attributeName", "transform")
    transform.setAttribute("type", "translate")
    transform.setAttribute("values", `0,${id < 3 ? -2 : 2};0,0`)
    transform.setAttribute("keySplines", "0 0 0.55 1")
    transform.setAttribute("calcMode", "spline")
    transform.setAttribute("begin", `${index * animationInterval}s`)
    transform.setAttribute("dur", `${animationDuration}s`)
    animationElements.appendChild(transform)

    fadeIn = createSVGNode("animate")
    setNSLinkToElement(fadeIn, `#ns${id}`)
    fadeIn.setAttribute("attributeName", "fill-opacity")
    fadeIn.setAttribute("attributeType", "XML")
    fadeIn.setAttribute("values", "0;1")
    fadeIn.setAttribute("calcMode", "spline")
    fadeIn.setAttribute("keySplines", "0 0 0.55 1")
    fadeIn.setAttribute("fill", "freeze")
    fadeIn.setAttribute("begin", `${index * animationInterval}s`)
    fadeIn.setAttribute("dur", `${animationDuration}s`)
    animationElements.appendChild(fadeIn)
})

let mainFadeIn
for (let k = 0; k <= 1; ++k) {
    mainFadeIn = createSVGNode("animate")
    setNSLinkToElement(mainFadeIn, `#stroke${k}`)
    mainFadeIn.setAttribute("attributeName", "stroke-dashoffset")
    mainFadeIn.setAttribute("attributeType", "XML")
    mainFadeIn.setAttribute("values", `${k ? 56.8 : 5.3};0`)
    mainFadeIn.setAttribute("calcMode", "spline")
    mainFadeIn.setAttribute("keySplines", k ? "0.55 0.06 0.76 0.18" : "0 0 0.55 1")
    mainFadeIn.setAttribute("fill", "freeze")
    mainFadeIn.setAttribute("begin", `${k ? 1.5 : 1.0}s`)
    mainFadeIn.setAttribute("dur", `${k ? 1.5 : 0.7}s`)
    animationElements.appendChild(mainFadeIn)
}

let fadeOut
for (let id = 0; id < 11; ++id) {
    fadeOut = createSVGNode("animate")
    setNSLinkToElement(fadeOut, id < 9 ? `#ns${id}` : `#stroke${id - 9}`)
    fadeOut.setAttribute("attributeName", id < 9 ? "fill-opacity" : "stroke-opacity")
    fadeOut.setAttribute("attributeType", "XML")
    fadeOut.setAttribute("values", "1;0")
    fadeOut.setAttribute("calcMode", "spline")
    fadeOut.setAttribute("keySplines", "0.45 0 1 1")
    fadeOut.setAttribute("fill", "freeze")
    fadeOut.setAttribute("begin", `${durationSum - animationDuration}s`)
    fadeOut.setAttribute("dur", `${animationDuration}s`)
    animationElements.appendChild(fadeOut)
}


const mainGroup = document.querySelector("#main")
mainGroup.appendChild(animationElements)
