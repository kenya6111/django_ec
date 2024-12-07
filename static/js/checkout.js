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
    postInputQuantity(itemId,itemCount)
  }
  let element = document.getElementById('item-price-sum');

  const displayRedeemPrice = document.getElementsByClassName('redeem-display')[0].getElementsByTagName('span')[0];
  if(displayRedeemPrice.textContent.substring(2).length >2){
    totalPrice = totalPrice - Number(displayRedeemPrice.textContent.substring(2))
    if (totalPrice <0) totalPrice=0
  }

  element.innerHTML = "$"+totalPrice;
}

async function postInputQuantity(itemId, itemCount){
  const csrftoken = Cookies.get('csrftoken');
  const postBody = {
      item_id: itemId,
      item_quantity: itemCount,
  };
  const postData = {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(postBody)
  };
  const res = await fetch("../updatecart/", postData)
}


async function deleteClick(itemId){
  const csrftoken = Cookies.get('csrftoken');
  const postBody = {
      item_id: itemId
  };
  const postData = {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(postBody)
  };
  const res = await fetch("../removefromcart/", postData)
  const data = await res.json()

  if (data.status === 'success') {
    console.log('成功:', data.message);

    const itemProduct = document.getElementById(`list-group-item-product-${itemId}`)
    itemProduct.remove()
    inputChange()
  } else {
    console.log('失敗:', data.message);
  }
}



async function redeemClick(){
  // 入力プロモーションコード取得
  const inputRedeem = document.getElementById('redeem-input').value
  debugger
  const csrftoken = Cookies.get('csrftoken');
  const postBody = {
      redeem_code: inputRedeem
  };
  const postData = {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(postBody)
  };
  // 入力プロモーションコードがDBに存在するかチェック
  const res = await fetch("../checkRedeem/", postData)
  const data = await res.json()
  if (data.status === 'success') {
    console.log('成功:', data.message);
    // 存在していた場合のUI更新
    document.getElementsByClassName('redeem-display')[0].classList.remove('d-none')

    // 入力プロモーションコードを画面表示
    const displayRedeemCode = document.getElementsByClassName('redeem-display')[0].getElementsByTagName('small')[0];
    displayRedeemCode.textContent=inputRedeem

    // 割引額を画面表示
    const displayRedeemPrice = document.getElementsByClassName('redeem-display')[0].getElementsByTagName('span')[0];
    displayRedeemPrice.textContent='-$'+data.redeem.discount_amount

    const hiddenRedeenPrice = document.getElementsByName('redeem-price')[0]
    hiddenRedeenPrice.value = data.redeem.discount_amount

    // 小計額から割引額を引く
    const itemPriceSumEle = document.getElementById('item-price-sum');
    itemPriceSumEle.textContent = Number(itemPriceSumEle.textContent.substring(1)) - data.redeem.discount_amount

  } else {
    console.log('失敗:', data.message);
    // 失敗時のUI更新
  }
}

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
