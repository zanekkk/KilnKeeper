
function addRow(minutes,temperature) {
    // (B1) GET TABLE
    var table = document.getElementById("scheduleNew");
    if (typeof steps !== 'undefined' && steps.length > 0) {
        stepNumber = steps.last()[0] + 1
    } else {
        stepNumber = 1
    }
    var row = table.insertRow(1);
    // (B3) INSERT CELLS
        cell = row.insertCell();
    cell.innerHTML = stepNumber;
    var cell = row.insertCell();
    cell.innerHTML = minutes;
    cell = row.insertCell();
    cell.innerHTML = temperature;
   }