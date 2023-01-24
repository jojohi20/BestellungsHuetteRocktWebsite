function chageAmount(value, id) {

    var currentAmount = parseInt(document.getElementById("amount" + id).value);
    console.log(currentAmount)
    var newAmount = currentAmount += value;
    console.log(newAmount);
    if(newAmount < 0) return;
    document.getElementById("amount" + id).value = newAmount;
    document.getElementById("amount-display" + id).innerHTML = "Menge: " + newAmount.toString();
}