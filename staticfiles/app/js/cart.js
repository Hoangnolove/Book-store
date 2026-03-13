var updateBtns = document.getElementsByClassName('update-cart')

for (let btn of updateBtns){
    btn.addEventListener('click', function(e){
        e.preventDefault()
        e.stopPropagation()

        updateUserOrder(
            this.dataset.product,
            this.dataset.action
        )
    })
}

function updateUserOrder(productId, action){
    fetch('/update_item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ productId, action })
    })
    .then(res => res.json())
    .then(data => {
        if (action === 'add') {
            showCartToast('Đã thêm sản phẩm vào giỏ hàng 🛒', 'success')
        }

        const cartTotal = document.getElementById('cart-total')
        if (cartTotal && data.cartItems !== undefined) {
            cartTotal.innerText = data.cartItems
        }
    })
    .catch(() => {
        showCartToast('Có lỗi xảy ra', 'danger')
    })
}


window.showCartToast = function (message, type = 'warning') {
    const toastEl = document.getElementById('cartToast')
    const toastBody = document.getElementById('cartToastBody')

    toastBody.innerText = message

    toastEl.classList.remove(
        'text-bg-success',
        'text-bg-danger',
        'text-bg-warning'
    )
    toastEl.classList.add(`text-bg-${type}`)

    new bootstrap.Toast(toastEl, { delay: 1500 }).show()
}