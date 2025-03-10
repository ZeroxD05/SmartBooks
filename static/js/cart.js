// Shopping cart functionality

document.addEventListener("DOMContentLoaded", function () {
  // Quantity input handlers
  const quantityInputs = document.querySelectorAll(
    'input[type="number"][name="quantity"]'
  );

  quantityInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      // Ensure quantity is at least 1
      if (parseInt(this.value) < 1) {
        this.value = 1;
      }
    });
  });

  // Size change price update on product page
  const sizeSelect = document.getElementById("size");
  if (sizeSelect) {
    const updatePrice = function () {
      const selectedOption = sizeSelect.options[sizeSelect.selectedIndex];
      const priceDisplay = document.getElementById("selected-price");
      if (priceDisplay) {
        priceDisplay.textContent = selectedOption.textContent.split(" - ")[1];
      }
    };

    sizeSelect.addEventListener("change", updatePrice);
    // Initialize on page load
    updatePrice();
  }

  // Form validation for checkout
  const checkoutForm = document.querySelector('form[action*="place_order"]');
  if (checkoutForm) {
    checkoutForm.addEventListener("submit", function (event) {
      const emailInput = document.getElementById("email");
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (emailInput && !emailPattern.test(emailInput.value)) {
        event.preventDefault();
        alert("Please enter a valid email address.");
        emailInput.focus();
      }

      const cardNumberInput = document.getElementById("card_number");
      if (cardNumberInput) {
        // Simple validation for demo purposes
        const cardNumber = cardNumberInput.value.replace(/\s/g, "");
        if (cardNumber.length < 16 || !/^\d+$/.test(cardNumber)) {
          event.preventDefault();
          alert("Please enter a valid card number (16 digits).");
          cardNumberInput.focus();
        }
      }

      const cvvInput = document.getElementById("cvv");
      if (cvvInput) {
        // Simple validation for demo purposes
        const cvv = cvvInput.value.trim();
        if (cvv.length < 3 || !/^\d+$/.test(cvv)) {
          event.preventDefault();
          alert("Please enter a valid CVV (3 or 4 digits).");
          cvvInput.focus();
        }
      }
    });
  }
});
