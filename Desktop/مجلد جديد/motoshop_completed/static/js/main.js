/* MotoShop offline JavaScript */
(function(){
"use strict";
window.toggleMobileMenu=function(){const m=document.getElementById("mobileMenu");if(!m)return;m.classList.toggle("hidden");document.body.classList.toggle("menu-open",!m.classList.contains("hidden"));};
function init(){
 const n=document.getElementById("navbar");const sc=()=>{if(n)n.classList.toggle("shadow-lg",window.scrollY>50)};sc();window.addEventListener("scroll",sc,{passive:true});
 const msg=document.getElementById("messages");if(msg)setTimeout(()=>{msg.style.opacity="0";msg.style.transition="opacity .4s ease";setTimeout(()=>msg.remove(),450)},5000);
 if("IntersectionObserver"in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("animate-fade-in-up");io.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll(".animate-on-scroll").forEach(e=>io.observe(e));}else document.querySelectorAll(".animate-on-scroll").forEach(e=>e.classList.add("animate-fade-in-up"));
 document.querySelectorAll("#mobileMenu a").forEach(a=>a.addEventListener("click",()=>{const m=document.getElementById("mobileMenu");if(m&&!m.classList.contains("hidden"))window.toggleMobileMenu()}));
 document.addEventListener("keydown",e=>{if(e.key==="Escape"){const m=document.getElementById("mobileMenu");if(m&&!m.classList.contains("hidden"))window.toggleMobileMenu()}});
 document.querySelectorAll("[data-range-sync]").forEach(r=>{const target=document.querySelector(r.dataset.rangeSync),out=document.querySelector(r.dataset.rangeOutput||"");const sync=()=>{if(target)target.value=r.value;if(out)out.textContent=Number(r.value).toLocaleString("ar-SA")};r.addEventListener("input",sync);sync();});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();