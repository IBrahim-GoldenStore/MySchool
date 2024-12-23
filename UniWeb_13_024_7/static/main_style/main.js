// #SCRIPTS POUR LE CHARGEMENT DYNAMIQUE

// let i=1

// document.addEventListener('DOMContentLoaded',function(){
//     Load_page(i)
// })

// let total_value= document.getElementById('button').value
// total_value= Number(total_value)
// console.log(total_value)

// const next= document.getElementById('next')
// const preview = document.getElementById('preview')

// if (total_value > 1){
//     preview.style.display='none'

//     console.log(total_value)
//     next.onclick= function(){
//         if( i >= 1 && i < total_value){
//             i+=1
//             Load_page(i)
//         }
//         preview.style.display='inline'
//         if(i == total_value){
//             next.style.display='none'
//         }
//     }
//     preview.onclick= function(){
//         if (i > 1 && i <= total_value){
//             i-=1
//             Load_page(i)
//         }
//         next.style.display='inline'
//         if (i==1){
//             preview.style.display='none'
//         }
//     }
// } else{
//     next.style.display='none'
//     preview.style.display='none'
// }

// function Load_page(page){
//     fetch('pagination/?page='+page)
//     .then(response => response.text())
//     .then(html => {
//         document.getElementById('container').innerHTML = html
//     })
//     return false
// }

document.addEventListener('DOMContentLoaded',function(){
    const menu_button= document.getElementById('menu-button')
    const menu_close= document.getElementById('menu-close')
    const nav_bar= document.querySelector('.nav-links') 
    menu_button.onclick= function(){
        nav_bar.classList.toggle('active')
    }
    menu_close.onclick=function(){
        nav_bar.classList.remove('active')
    }
    window.addEventListener('scroll',function(){
        if (window.scrollY > 200){
            nav_bar.classList.remove('active')
        }        
    })
})

document.addEventListener('DOMContentLoaded',function(){
    const send_button= document.getElementById('submit-button')
    const loading= document.querySelector('.show-load')
    send_button.onclick= function(){
        const interval=setInterval(()=>{
            loading.style.display='flex'
        },10)

        setTimeout(()=>{
            loading.style.display='none'
            clearInterval(interval)
        },35000)
    }
})
