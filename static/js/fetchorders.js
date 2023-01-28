
store = document.currentScript.getAttribute('store'); // 1
function getOrders(){
    fetch('/getOrders' + store)
    .then(response => response.json())
    .then(data => {


        const tableBody = document.querySelector('table > tbody');
       
        tableBody.innerHTML = '';

        Object.values(data).forEach(order => {

            const row = document.createElement('tr');

            const timeCell = document.createElement('td');
            timeCell.className = "orders-tabel";
            timeCell.innerHTML = order.displayTime;

            const storeCell = document.createElement('td');
            storeCell.className = "orders-tabel";
            storeCell.innerHTML = order.store;

            const itemsCell = document.createElement('td');
            itemsCell.className = "orders-tabel";
            order.items.forEach((item, i) => {
                itemsCell.innerHTML += `${order.amounts[i]}x ${item}<br>`;
            });

            const actionsCell = document.createElement('td');
            actionsCell.className = "orders-tabel";

            if(store == "") {
                actionsCell.innerHTML = `<a href="/done/${order.id}" class="bg-gray-800 p-2 rounded-xl">Erledigt</a>`;
            }
            else {
                actionsCell.innerHTML = `<a href="/cancel/${order.id}${store}" class="bg-gray-800 p-2 rounded-xl">Abbrechen</a>`;
            }
            
            row.appendChild(timeCell);
            if(store == "") {
                row.appendChild(storeCell);
            }
            row.appendChild(itemsCell);
            row.appendChild(actionsCell);

            tableBody.appendChild(row);
        });
    });
}

getOrders()
setInterval(() => {
    getOrders()
}, 5000);