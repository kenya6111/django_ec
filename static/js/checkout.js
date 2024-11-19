// ele = document.getElementsByClassName('form-select')
// console.log(ele)
// // 各要素に対してイベントリスナーを追加
// for (let i = 0; i < ele.length; i++) {
//   ele[i].onchange = event => {
//     // console.log(999);  // 値が変更されたときに呼ばれる
//     // console.log("Selected Value:", event.target.value);
//     // let selectedQuantity = event.target.value;
//     // // let itemPriceSUm = document.getElementById('item-price-sum')
//     //   // 選択された値を表示
//     // objId = event.target.id.slice(-1)
//     // itemPrice = document.getElementsByClassName(`item-price-${objId}`)


//     newPriceSum=0
//     listGroupItems = document.getElementsByClassName('list-group-item-product')
//     for( let i=0; i <listGroupItems.length; i++){
//       console.log(listGroupItems[i])
//       let itemId = listGroupItems[i].getElementsByClassName('item-id')[0].value
//       // let itemCount = document.getElementsByClassName('list-group-item')[0].getElementsByClassName('item-count')[0].value
//       let itemCount = document.getElementById(`select-box-${itemId}`).value
//       let itemPrice = document.getElementById(`item-price-${itemId}`).value
//       newPriceSum += itemCount*itemPrice
//     }
//     console.log(newPriceSum)
//     document.getElementById('item-price-sum').textContent = newPriceSum
    



//   };
// }

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