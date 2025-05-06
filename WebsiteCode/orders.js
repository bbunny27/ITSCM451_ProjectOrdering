window.onload = async function () {
    const token = localStorage.getItem("idToken");
    if (!token) {
        alert("You must be logged in to view your orders.");
        window.location.href = "index.html";
        return;
    }

    try {
        const response = await fetch("https://api.capybaraparadise.xyz/orders", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const orders = await response.json();
        const ordersDiv = document.getElementById("orders");

        if (orders.length === 0) {
            ordersDiv.innerHTML = "<p>No past orders found.</p>";
            return;
        }

        orders.forEach(order => {
            const div = document.createElement("div");
            div.className = "order";
            div.innerHTML = `<strong>${order.item_id}</strong> x${order.quantity} on ${new Date(order.timestamp).toLocaleString()}`;
            ordersDiv.appendChild(div);
        });

    } catch (err) {
        console.error("Failed to load orders:", err);
        alert("Error loading orders");
    }
};
