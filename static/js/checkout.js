function inputChange(){
  eles = document.getElementsByClassName('list-group-item-product')
  totalPrice = 0;
  for (let i = 0; i < eles.length; i++) {
    itemId = eles[i].getElementsByClassName('item-id')[0].value
    itemCount = document.getElementById(`select-box-${itemId}`).value

    isSale = eles[i].getElementsByClassName('is_sale')[0].value === 'True'
    itemPrice = parseFloat(document.getElementById(`item-price-${itemId}`).value);
    if(isSale)
    {
      totalPrice += itemPrice*0.6*itemCount
    }else
    {
      totalPrice += itemPrice*itemCount
    }
  }
  let element = document.getElementById('item-price-sum');
  element.innerHTML = "$"+totalPrice;

}


  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  (function() {
    const formsuuu = document.querySelectorAll('.needs-validation');
    formsuuu.forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      });
    });
  })();
