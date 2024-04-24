let subMenu = document.getElementById("profile-subMenu")

function toggleMenu() {
    subMenu.classList.toggle("open-menu")
}


function updateCartCount() {
    var cartCount = document.querySelector('.cart-count');
    fetch('http://127.0.0.1:8000/fetch-cart-count')
        .then(response => response.json())
        .then(data => {
            cartCount.textContent = data.cart_count;
        });
}

updateCartCount();

