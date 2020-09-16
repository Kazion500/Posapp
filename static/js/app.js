/** @format */

$(document).ready(function () {


  if ($('#message_error').html() !== undefined){
    setTimeout(()=>{
      $('#message_error').remove()
    },4000)
  }

  
  // js for sales

  let change = $("#change");
  let amount_given = $(".amount-given");
  let config_discount = $("#config-discount");
  let total_price = $("#sales-total-price");
  let quantity = $("#quantity");
  let discount = $("#sales-discount");
  let salesPrice = $("#sales-price");
  let config_quantity = $("#config-quantity");
  const maxDicount = 100;
  let numChange;

  // initializer function

  salesProcessCalc();

  function salesProcessCalc() {
    getQuantity();
    setDiscount();
    CalcChange();
  }

  function customFunc(amountInput, config) {
    config.on("input", () => {
      if (config.val() === "" || config.val() == Number("")) {
        amountInput.val("");
      } else {
        if (Number(config.val())) {
          Number(amountInput.val(config.val()));
        }
      }
    });
  }


  // quantity calculations
  function getQuantity() {
    customFunc(quantity, config_quantity);

    config_quantity.on("input", () => {
      let quantityVal = Number(quantity.val());
      let priceVal = Number(salesPrice.val());
      if (config_quantity.val() === "" || config_quantity.val() == Number("")) {
        total_price.val("");
        config_discount.val("");
      }
      if (quantityVal) {
        let totalPrice = priceVal * quantityVal;
        totalPriceVal = Number(total_price.val(totalPrice));
      }
    });
  }


  // calculate discount

  function setDiscount() {
    customFunc(discount, config_discount);

    config_discount.on("input", () => {
      if (config_quantity.val() === "" || config_quantity.val() == Number("")) {
        config_discount.val("");

        discount.val("");
      } else if (
        config_quantity.val() !== "" ||
        config_quantity.val() != Number("")
      ) {
        const numDiscount = Number(discount.val());

        const totalPrice = Number(total_price.val());

        if (totalPrice > numDiscount) {
          if (config_discount.val() === "") {
            let quantityVal = Number(quantity.val());

            let priceVal = Number(salesPrice.val());

            let totalPrice = priceVal * quantityVal;

            totalPriceVal = Number(total_price.val(totalPrice));

            Number(total_price.val());
          } else {
            const actualPrice =
              Number(salesPrice.val()) * Number(quantity.val()) - numDiscount;

            Number(total_price.val(actualPrice));
          }
        } else {
          discount.val(maxDicount);

          if (Number(config_discount.val()) || Number(config_quantity.val())) {
            $("#erro").html(
              `<h4 class='alert alert-danger p-2'>Discount shouldn't exceed ${maxDicount} </h4>`
            );

            setTimeout(() => {
              $("#erro").html("");
            }, 3000);
          }
        }
      }
    });
  }

  // Calculate Change

  function CalcChange() {
    amount_given.on("input", () => {
      const numAmtGiven = Number(amount_given.val());

      const numTotalPrice = Number(total_price.val());

      if (numAmtGiven > numTotalPrice) {
        numChange = numAmtGiven - numTotalPrice;
      } else {
        numChange = "";
      }

      if (total_price.val() !== "" || total_price.val() != Number("")) {
        if (numChange != "") {
          change.html(
            `<h4 class='alert alert-success'>Customers Change is K${numChange}</h4>`
          );

          setTimeout(() => {
            change.html("");
          }, 7000);
        }
      } else {
        change.html("");
      }
    });
  }
  // Ajax Call for stockProduct

  let sales_product_name_input = $("#sales_product_name_input");
  let salesCategoryId = $("#sales_category_id");
  let salesProductId = $("#sales_product_id");

  $(sales_product_name_input).change(function () {
    sales_total = "";
    $.ajax({
      type: "GET",
      url: "",
      data: {
        StockName: $(this).val(),
      },
      success: function (response) {
        salesProductId.val(response.product_id);

        let sales_price = salesPrice.val(response.product_price);
        $("#placeholder_product_name").val(response.product_name);

        let sales_cat_id = salesCategoryId.val(response.category_id);
        if (sales_cat_id.val() === "NaN") {
          sales_cat_id.val("");
          sales_price.val("");
        }
        if (sales_product_name_input.val() === "") {
          salesProductId.val("");
          salesCategoryId.val("");
          salesPrice.val("");
        }
      },
    });
  });

  // stocks quantity

  let stock_qty = $(".stock_qty");
  let classes = [
    "badge badge-danger",
    "badge badge-warning",
    "badge badge-success",
  ];

  stock_qty.each((i, val) => {
    qty = val.innerHTML;
    if (qty == 0) {
      r = val.nextElementSibling.innerHTML = `<span class="${classes[0]}">Out of Stock</span>`;
    } else if (qty <= 5) {
      r = val.nextElementSibling.innerHTML = `<span class="${classes[1]}">Low in Stock</span>`;
    } else if (qty > 5) {
      r = val.nextElementSibling.innerHTML = `<span class="${classes[2]}">In Stock</span>`;
    } else {
      r = val.nextElementSibling.innerHTML = "";
    }
  });

});
