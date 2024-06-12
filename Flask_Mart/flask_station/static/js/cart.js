$(document).ready(function () {
  getCartItems();
  $(document).on("click", ".add-to-cart-btn", function (e) {
    e.preventDefault();
    var productId = $(this).data("product-id");

    $.ajax({
      url: "/add_to_cart/" + productId,
      type: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      data: JSON.stringify({ product_id: productId }),
      contentType: "application/json",
      success: function (response) {
        if (response.success) {
          alert("cart updated successfully");
          getCartItems();
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
  var cartContainer = document.getElementById("cart-container");
  var checkoutContainer = document.getElementById("checkout");
  // Clear the existing contents of the cart container
  cartContainer.innerHTML = "";
  let amountInCart = 0

  if (cartItems && cartItems[0]?.title) {
    // Iterate over the cartItems array
    amountInCart = getTotalPriceInCart(cartItems)
    const amountInCartInDollars = `$${(amountInCart ? (Math.round(amountInCart * 100) / 100).toFixed(2) : "0.00")}`;
    cartItems.forEach(function (item) {
      // Create HTML elements to represent each cart item
      var cartItemDiv = document.createElement("div");
      cartItemDiv.classList.add("cart-item", "my-2", "bg-light", "p-2");

      var productImage = document.createElement("img");
      productImage.src = "/static/post_pics/" + item.image;
      productImage.classList.add("product-image", "img-fluid");
      productImage.alt = "";
      cartItemDiv.appendChild(productImage);

      // var divider = document.createElement("hr");
      // cartItemDiv.appendChild(divider);


      var flexDiv = document.createElement("div");
      flexDiv.classList.add("d-md-flex", "justify-content-between", "pt-2");



      var productName = document.createElement("p");
      productName.textContent = item.title;
      flexDiv.appendChild(productName);

      var productPrice = document.createElement("p");
      productPrice.textContent = `$${item.price}`;
      flexDiv.appendChild(productPrice);

      cartItemDiv.appendChild(flexDiv);


      var quantity = document.createElement("p");
      quantity.textContent = "Quantity: " + item.quantity;
      cartItemDiv.appendChild(quantity);

      // Create plus and minus buttons for adjusting quantity
      var plusButton = document.createElement("button");
      plusButton.textContent = "+";
      plusButton.classList.add("quantity-button", "btn");
      plusButton.addEventListener("click", function () {
        // Call a function to increase quantity of this item
        increaseQuantity(item.product_id);
      });
      cartItemDiv.appendChild(plusButton);

      var minusButton = document.createElement("button");
      minusButton.textContent = "-";
      minusButton.classList.add("quantity-button", "ml-2", "btn");
      minusButton.addEventListener("click", function () {
        // Call a function to decrease quantity of this item
        decreaseQuantity(item.product_id);
      });
      cartItemDiv.appendChild(minusButton);

      // Create a remove button
      var removeButton = document.createElement("button");
      removeButton.textContent = "Remove";
      removeButton.classList.add(
        "remove-button",
        "ml-2",
        "btn",
        "btn-outline-danger"
      );
      removeButton.addEventListener("click", function () {
        // Call a function to remove this item from the cart
        removeFromCart(item.product_id);
      });
      cartItemDiv.appendChild(removeButton);
      // cartItemDiv.appendChild(divider);

      // Append the cart item element to the cart container
      cartContainer.appendChild(cartItemDiv);
      var checkoutButton = document.createElement("button");
     

      checkoutButton.classList.add("btn", "btn-outline-info")
      checkoutButton.innerHTML = "Checkout";

    });
    var checkoutPriceElem = document.getElementById("amount-in-cart");
    checkoutPriceElem.textContent = amountInCartInDollars
    checkoutContainer.classList.remove("d-none");
    checkoutContainer.classList.add("d-flex");
    
    // checkoutContainer.appendChild(checkoutPriceElem)
    // checkoutContainer.appendChild(checkoutButton)
  } else {
    var empty = document.createElement("p");
    checkoutContainer.classList.add("d-none");
    checkoutContainer.classList.remove("d-flex");
    empty.textContent = "Your cart is empty";
    cartContainer.appendChild(empty);
    var cartItemDiv = document.createElement("div");
    cartItemDiv.classList.add("cart-bg");
    cartContainer.appendChild(cartItemDiv);
  }
}

function getCartItems() {
  $.ajax({
    url: "/cart_items",
    type: "GET",
    success: function (response) {
      // Handle successful response
      // Update the cart UI with the retrieved cart items
      updateCartUI(response);
    },
    error: function (error) {
      // Handle error
      console.error("Error retrieving cart items:", error);
    },
  });
}

// Function to handle increasing the quantity of an item in the cart
function increaseQuantity(product_id) {
  fetch(`/increase_quantity/${product_id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Update the UI to reflect the change in quantity
        getCartItems();
      } else {
        // Handle error, display error message, etc.
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Function to handle decreasing the quantity of an item in the cart
function decreaseQuantity(product_id) {
  fetch(`/decrease_quantity/${product_id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Update the UI to reflect the change in quantity
        getCartItems(true);
      } else {
        // Handle error
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Function to handle removing an item from the cart
function removeFromCart(product_id) {
  fetch(`/remove_from_cart/${product_id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        getCartItems(true);
        // Update the UI to reflect the removal of the item
      } else {
        // Handle error
      }
    })
    .catch((error) => console.error("Error:", error));
}

function getTotalPriceInCart(cartItems){
  return cartItems.reduce((a, b) => a += +b.price * b.quantity, 0)
}
