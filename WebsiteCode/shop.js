let cart = [];

async function loadInventory() {
    try {
        const res = await fetch("https://api.capybaraparadise.xyz/inventory");
        const inventory = await res.json();

        const container = document.getElementById('inventory');
        container.innerHTML = '';

        inventory.forEach(item => {
            const itemDiv = document.createElement('div');
            itemDiv.innerHTML = `
                <h2>${item.name}</h2>
                <p>Available: ${item.quantity}</p>
                <button onclick="addToCart('${item.item_id}', '${item.name}')">Add to Cart</button>
                <hr>
            `;
            container.appendChild(itemDiv);
        });
    } catch (err) {
        console.error("Failed to load inventory:", err);
    }
}

function addToCart(itemId, itemName) {
    const existingItem = cart.find(item => item.item_id === itemId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ item_id: itemId, name: itemName, quantity: 1 });
    }
    renderCart();
}

function renderCart() {
    const cartDiv = document.getElementById('cart');
    cartDiv.innerHTML = '';

    if (cart.length === 0) {
        cartDiv.innerHTML = '<p>Your cart is empty.</p>';
        return;
    }

    cart.forEach(item => {
        const div = document.createElement('div');
        div.innerHTML = `
            <h3>${item.name}</h3>
            <p>Quantity: ${item.quantity}</p>
        `;
        cartDiv.appendChild(div);
    });
}

async function checkout() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    const idToken = localStorage.getItem('idToken');
    if (!idToken) {
        alert("You must be logged in to place an order!");
        return;
    }

    try {
        for (const item of cart) {
            const response = await fetch("https://api.capybaraparadise.xyz/order", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${idToken}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    item_id: item.item_id,
                    quantity: item.quantity
                })
            });

            if (!response.ok) {
                throw new Error(`Order failed for item ${item.item_id}`);
            }
        }

        document.getElementById('msg').innerText = "✅ Your order has been placed!";
        cart = [];
        renderCart();
        loadInventory(); // reload available inventory
    } catch (error) {
        console.error("Order error:", error);
        document.getElementById('msg').innerText = "❌ Failed to place order. Please try again.";
    }
}

// Load inventory when page loads
window.onload = loadInventory;

