const navSlider = () => {
    const sandwich = document.querySelector(".sandwich");
    const navi = document.querySelector(".nav-links");
    const links = document.querySelectorAll(".nav-links li");

    sandwich.addEventListener("click", () => {
        navi.classList.toggle("nav-active");

        links.forEach((link, index) => {
            if(link.style.animation){
                link.style.animation = "";
            }
            else {
                link.style.animation = "linkFadeIn 0.5s ease forwards ${ index / 7 + 0.3 }s";
            }
        });

        sandwich.classList.toggle("cross");
    });
}

const openConfirm = () => {
    let confirm = document.querySelector(".confirm-container");
    if (!confirm.classList.contains("confirm-open")){
        confirm.classList.add("confirm-open");
    }
}

const closeConfirm = () => {
    let confirm = document.querySelector(".confirm-container");
    if (confirm.classList.contains("confirm-open")){
        confirm.classList.remove("confirm-open");
    }
}

const app = ()=>{
    navSlider();
}

app()

