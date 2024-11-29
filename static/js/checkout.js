function inputChange(){
  eles = document.getElementsByClassName('list-group-item-product')
  totalPrice = 0;
  for (let i = 0; i < eles.length; i++) {
    console.log(eles[i])
    itemId = eles[i].getElementsByClassName('item-id')[0].value
    console.log(itemId+":itemId");
    itemCount = document.getElementById(`select-box-${itemId}`).value
    console.log(itemCount+":itemcount");

    isSale = eles[i].getElementsByClassName('is_sale')[0].value === 'True'
    console.log(isSale+":issale");
    
    itemPrice = parseFloat(document.getElementById(`item-price-${itemId}`).value);
    console.log(itemPrice+":itemprice");
    
    if(isSale)
    {
      totalPrice += itemPrice*0.6*itemCount
    }else
    {
      totalPrice += itemPrice*itemCount
      console.log(totalPrice+"totalprice");
    }
  }
  console.log(totalPrice+"totalprice")
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
