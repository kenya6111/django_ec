ele = document.getElementsByClassName('form-select')
console.log(ele)
// 各要素に対してイベントリスナーを追加
for (let i = 0; i < ele.length; i++) {
  ele[i].onchange = event => {
    // console.log(999);  // 値が変更されたときに呼ばれる
    // console.log("Selected Value:", event.target.value);
    // let selectedQuantity = event.target.value;
    // // let itemPriceSUm = document.getElementById('item-price-sum')
    //   // 選択された値を表示
    // objId = event.target.id.slice(-1)
    // itemPrice = document.getElementsByClassName(`item-price-${objId}`)


    newPriceSum=0
    listGroupItems = document.getElementsByClassName('list-group-item-product')
    for( let i=0; i <listGroupItems.length; i++){
      console.log(listGroupItems[i])
      let itemId = listGroupItems[i].getElementsByClassName('item-id')[0].value
      // let itemCount = document.getElementsByClassName('list-group-item')[0].getElementsByClassName('item-count')[0].value
      let itemCount = document.getElementById(`select-box-${itemId}`).value
      let itemPrice = document.getElementById(`item-price-${itemId}`).value
      newPriceSum += itemCount*itemPrice
    }
    console.log(newPriceSum)
    document.getElementById('item-price-sum').textContent = newPriceSum
    



  };
}