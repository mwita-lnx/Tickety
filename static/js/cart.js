 yourText = `<div><button
      type="button"
      id=""
      class="btn btn-primary"
      data-toggle="modal"
      data-target="#cart"
      style="margin:5px;"
    >
      Cart (<span class="total-count"></span>)</a>
      <button class="clear-cart btn btn-danger" ;">Clear Cart</button>
     `;

$(".men").append(yourText);

const csrftoken = document.querySelector(
"[name=csrfmiddlewaretoken]"
).value;
function postToDb(ticket_type,price) {
let _data = {
  "id": 1,
  "username": "Lennox mwita",
  "price": price,
  "serial_no": "ooooooooo",
  "ticket_type": ticket_type,
  "saved": true,
  "User": 1,
  "event": 1
};

$.ajax({
url: "/api/ticket/create",
type: "POST",
dataType: "json",
data: _data,
headers: { "X-CSRFToken": csrftoken },

success: function (data, textStatus, xhr) {
  console.log(data);
},
error: function (xhr, textStatus, errorThrown) {
  console.log(xhr+textStatus+errorThrown);
},
});
}

var shoppingCart = (function () {
// =============================
// Private methods and propeties
// =============================
cart = [];

// Constructor
function Item(name, price, count) {
this.name = name;
this.price = price;
this.count = count;
}

// Save cart
function saveCart() {
sessionStorage.setItem("shoppingCart", JSON.stringify(cart));
}

// Load cart
function loadCart() {
cart = JSON.parse(sessionStorage.getItem("shoppingCart"));
}
if (sessionStorage.getItem("shoppingCart") != null) {
loadCart();
}

// =============================
// Public methods and propeties
// =============================
var obj = {};

// Add to cart
obj.addItemToCart = function (name, price, count) {
for (var item in cart) {
  if (cart[item].name === name) {
    cart[item].count++;
    saveCart();
    return;
  }
}
var item = new Item(name, price, count);
cart.push(item);
saveCart();
};
// Set count from item
obj.setCountForItem = function (name, count) {
for (var i in cart) {
  if (cart[i].name === name) {
    cart[i].count = count;
    break;
  }
}
};
// Remove item from cart
obj.removeItemFromCart = function (name) {
for (var item in cart) {
  if (cart[item].name === name) {
    cart[item].count--;
    if (cart[item].count === 0) {
      cart.splice(item, 1);
    }
    break;
  }
}
saveCart();
};

// Remove all items from cart
obj.removeItemFromCartAll = function (name) {
for (var item in cart) {
  if (cart[item].name === name) {
    cart.splice(item, 1);
    break;
  }
}
saveCart();
};

// Clear cart
obj.clearCart = function () {
cart = [];
saveCart();
};

// Count cart
obj.totalCount = function () {
var totalCount = 0;
for (var item in cart) {
  totalCount += cart[item].count;
}
return totalCount;
};

// Total cart
obj.totalCart = function () {
var totalCart = 0;
for (var item in cart) {
  totalCart += cart[item].price * cart[item].count;
}
return Number(totalCart.toFixed(2));
};

// List cart
obj.listCart = function () {
var cartCopy = [];
for (i in cart) {
  item = cart[i];
  itemCopy = {};
  for (p in item) {
    itemCopy[p] = item[p];
  }
  itemCopy.total = Number(item.price * item.count).toFixed(2);
  cartCopy.push(itemCopy);
}

return cartCopy;
};

// cart : Array
// Item : Object/Class
// addItemToCart : Function
// removeItemFromCart : Function
// removeItemFromCartAll : Function
// clearCart : Function
// countCart : Function
// totalCart : Function
// listCart : Function
// saveCart : Function
// loadCart : Function
return obj;
})();

// *****************************************
// Triggers / Events
// *****************************************
// Add item
$(".add-to-cart").click(function (event) {
event.preventDefault();
var name = $(this).data("name");
var price = Number($(this).data("price"));
shoppingCart.addItemToCart(name, price, 1);
displayCart();
});

$(".place-order").click(function (event) {

cart = shoppingCart.listCart();
for (var i in cart) {

var category_name = cart[i].name;
var cartegory_price = cart[i].price;
var no_of_tickets = cart[i].count;
for (let j = 0; j < no_of_tickets; j++) {
  postToDb(category_name,cartegory_price)


}
}

displayCart();
if($(".show-cart").html() == ''){
$(".show-cart").html('<h1>No order To be placed </h1>');
}
else{
$(".show-cart").html('<h1>Order has been completed</h1>');
$(".place-order").html('finished')
var total = shoppingCart.totalCart()
$(".total-cart").html(total);
shoppingCart.clearCart();
displayCart();
}

});

// Clear items
$(".clear-cart").click(function () {
shoppingCart.clearCart();

displayCart();
});

function displayCart() {
var cartArray = shoppingCart.listCart();
var output = "";
for (var i in cartArray) {
output +=
  "<tr>" +
  "<td>" +
  cartArray[i].name +
  "</td>" +
  "<td>(" +
  cartArray[i].price +
  ")</td>" +
  "<td><div class='input-group'><button class='minus-item input-group-addon btn btn-primary' data-name=" +
  cartArray[i].name +
  ">-</button>" +
  "<input type='number' class='item-count form-control' data-name='" +
  cartArray[i].name +
  "' value='" +
  cartArray[i].count +
  "'>" +
  "<button class='plus-item btn btn-primary input-group-addon' data-name=" +
  cartArray[i].name +
  ">+</button></div></td>" +
  "<td><button class='delete-item btn btn-danger' data-name=" +
  cartArray[i].name +
  ">X</button></td>" +
  " = " +
  "<td>" +
  cartArray[i].total +
  "</td>" +
  "</tr>";
}
$(".show-cart").html(output);
$(".total-cart").html(shoppingCart.totalCart());
$(".total-count").html(shoppingCart.totalCount());
}

// Delete item button

$(".show-cart").on("click", ".delete-item", function (event) {
var name = $(this).data("name");
shoppingCart.removeItemFromCartAll(name);
displayCart();
});

// -1
$(".show-cart").on("click", ".minus-item", function (event) {
var name = $(this).data("name");
shoppingCart.removeItemFromCart(name);
displayCart();
});
// +1
$(".show-cart").on("click", ".plus-item", function (event) {
var name = $(this).data("name");
shoppingCart.addItemToCart(name);
displayCart();
});

// Item count input
$(".show-cart").on("change", ".item-count", function (event) {
var name = $(this).data("name");
var count = Number($(this).val());
shoppingCart.setCountForItem(name, count);
displayCart();
});

displayCart();