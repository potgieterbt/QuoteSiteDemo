var input, filter, table, tr, td, i, txtValue, found;

function myFunction() {
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    filters = filter.split(" ");
    for (i = 0; i < tr.length; i++) {
        found = false;
        td = tr[i].getElementsByTagName("td")[0];
        td1 = tr[i].getElementsByTagName("td")[1];
        if (td) {
            txtValue = td.textContent || td.innerText;
            txtValue2 = td1.textContent || td1.innerText;
            console.log(filters)
            filters.forEach(function (filter) {
                console.log(filter);
                if (filter === "") {
                    console.log("null")
                    found = true;
                } else if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    console.log("match on title")
                    found = true;
                } else if (txtValue2.toUpperCase().indexOf(filter) > -1) {
                    console.log("match on code")
                    found = true;
                }
                if (found === true) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            });
        }
    }
}