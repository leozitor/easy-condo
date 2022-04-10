window.addEventListener("load", function () {
    let footer = document.querySelector(".footer")
    let formUser = document.querySelector("#id_username")
    let formPassword = document.querySelector("#id_password")


    formUser.classList.add("form-control", "p-2")
    formUser.placeholder = "Email Address"
    formPassword.classList.add("form-control", "p-2")
    formPassword.placeholder = "Password"
    footer.classList.remove("bg-light")
});

