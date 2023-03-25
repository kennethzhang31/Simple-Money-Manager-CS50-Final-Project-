today = new Date();
currentMonth = today.getMonth();
currentYear = today.getFullYear();

calendar = document.getElementById("calendar");
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
days = ["Sun", "Mon", "Tues", "Wed", "Thu", "Fri", "Sat"];

var tablerows ="<tr>";
for (day in days){
    tablerows += "<th data-day='" + days[day] + "'>" + days[day] + "</th>";
}
tablerows += "</tr>";

document.getElementById("thead-main").innerHTML = tablerows;

monthYear = document.getElementById("monthYear");
calendarShow(currentMonth, currentYear);

function daysInMonth(month, year) {
    return new Date(year, month + 1, 0).getDate();
}

function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    calendarShow(currentMonth, currentYear);
}
function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    calendarShow(currentMonth, currentYear);
}

function calendarShow(month, year){
    var day = new Date(year, month);
    var firstday = day.getDay();

    var table = document.getElementById("calendar-body");
    table.innerHTML = "";

    monthYear.innerHTML = months[month] + " " + year;

    let date = 1;
    const numOfDays = daysInMonth(month, year);
    for (var i = 0; i<6; i++){
        var calendarRow = document.createElement("tr");

        for (var j = 0; j < 7; j++){
           if (i === 0 && j < firstday){
                node = document.createElement("td");
                var cellText = document.createTextNode("");

                node.appendChild(cellText);
                calendarRow.appendChild(node);
            }
            else if (date > numOfDays){
                break;
            }
            else{
                const node = document.createElement("td");

                var formattedDate = ("0" + date).slice(-2);
                console.log(formattedDate);
                var formattedMonth = ("0" + (month+1)).slice(-2);

                node.setAttribute("data-date", formattedDate);
                node.setAttribute("data-month", formattedMonth);
                node.setAttribute("data-year", year);
                node.setAttribute("data-month-name", months[month]);

                idName = "date-" + formattedDate;

                node.setAttribute("id", idName);
                node.setAttribute("onclick", "lookup(this)");
                node.className = "date-picker";
                node.innerHTML = "<span>" + date + "</span>";

                if ( date === today.getDate() && year === today.getFullYear() && month === today.getMonth() ) {
                    node.className = "date-picker selected";
                }
                calendarRow.appendChild(node);
                date++;
            }
        }
        table.appendChild(calendarRow);
    }
}
