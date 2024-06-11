$(document).ready(function () {
  console.log("ready");
  $.ajax({
    url: "/cart_items",
    type: "GET",
    success: function (response) {
      // Handle successful response
      console.log("Cart items:", response);
      // Update the cart UI with the retrieved cart items
      updateCartUI(response);
    },
    error: function (error) {
      // Handle error
      console.error("Error retrieving cart items:", error);
    },
  });
  $(document).on("click", ".add-to-cart-btn", function (e) {
    e.preventDefault();
    console.log("clicked");
    var productId = $(this).data("product-id");
    console.log(productId, "productId");

    $.ajax({
      url: "/add_to_cart/" + productId,
      // url: `{{ url_for('main.add_to_cart', product_id=1) }}`,
      type: "POST",
      data: JSON.stringify({ product_id: productId }),
      // headers:
      contentType: "application/json",
      success: function (response) {
        console.log(response, "response"); // Log the response for debugging
        if (response.success) {
          // Update the cart contents section
          alert("cart updated successfully");
          $("#cart-contents").load(location.href + " #cart-contents>*", "");
        } else {
          // alert('Error adding to cart');
        }
      },
      error: function (xhr, status, error) {
        console.log(xhr.responseText); // Log the error response for debugging
        alert("Error adding to cart");
      },
    });
  });
});

function updateCartUI(cartItems) {
  // Get the element where you want to display the cart contents

  if (cartItems && cartItems[0]?.title) {
    console.log(cartItems, "cartItems");
    var cartContainer = document.getElementById("cart-container");
    // Clear the existing contents of the cart container
    cartContainer.innerHTML = "";

    // Iterate over the cartItems array
    cartItems.forEach(function (item) {
      // Create HTML elements to represent each cart item
      var cartItemDiv = document.createElement("div");
      cartItemDiv.classList.add("cart-item");

      var productImage = document.createElement("img");
      productImage.src = "/static/uploads/" + item.image;
      // productImage.width = "200px";
      // productImage.height = "200px";
      productImage.classList.add("product-image");
      productImage.alt = "";
      cartItemDiv.appendChild(productImage);

      var productName = document.createElement("p");
      productName.textContent = item.title;
      cartItemDiv.appendChild(productName);

      var quantity = document.createElement("p");
      quantity.textContent = "Quantity: " + item.quantity;
      cartItemDiv.appendChild(quantity);

      // Append the cart item element to the cart container
      cartContainer.appendChild(cartItemDiv);
    });
  }
}
