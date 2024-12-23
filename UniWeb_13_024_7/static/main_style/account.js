// compte.html
// ---------
//  sigin.html
document.addEventListener('DOMContentLoaded',function(){
    const username= document.getElementById('id_username')
    const password1= document.getElementById('id_password1')
    const password2= document.getElementById('id_password2')
    const email= document.getElementById('id_email')
    const hide= document.getElementById('hide')
    hide.addEventListener('click',function(){
        if(password1.type=='password' && password2.type=='password'){
            password1.type='text'
            password2.type='text'
        } else{
            password1.type='password'
            password2.type='password'
        }
    })
    username.placeholder="Nom d'utilisateur"
    password1.placeholder="Mot de passe"
    password2.placeholder="Confirmer votre mot de passe"
    email.placeholder="Email"
})
// login.html
document.addEventListener('DOMContentLoaded',function(){
    const username= document.getElementById('id_username')
    const password= document.getElementById('id_password')

    username.placeholder="Nom d'utilisateur"
    password.placeholder="Mot de passe"

    const hide= document.getElementById('hide_login')
    hide.addEventListener('click',function(){
        if(password.type=='password'){
            password.type='text'
        } else{
            password.type='password'
        }
    })
})
// update_bio.html
document.addEventListener('DOMContentLoaded',function(){
    const university = document.getElementById('id_university')
    const cycle = document.getElementById('id_cycle')
    const filiere = document.getElementById('id_filiere')
    university.placeholder= 'Université'
    // university.value=''
    cycle.placeholder= 'Cycle'
    // cycle.value=''
    filiere.placeholder='Filière'
    // filiere.value=''
    
})
//  newpassword.html
document.addEventListener('DOMContentLoaded',function(){
    const password1= document.getElementById('id_new_password1')
    const password2= document.getElementById('id_new_password2')
    const hide= document.getElementById('hide_password')

    password1.placeholder='Nouveau mot de passe'
    password2.placeholder='Confirmer votre mot de passe'

    hide.addEventListener('click',function(){
        if(password1.type=='password'){
            password1.type='text'
            password2.type='text'
        } else{
            password1.type='password'
            password2.type='password'
        }
    })
})
//  ask_email
document.addEventListener('DOMContentLoaded',function(){
    const email= document.getElementById('id_email')
    email.placeholder= "Entrez votre email"
})
// traitement du menu deroulant
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
