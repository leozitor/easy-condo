//All methods and calls are at the end


//create usage to post the booked session

class Activity {
    constructor(date, quantity, label, id, type, qtlimit) {
        this._date = date;
        this._label = label
        this._quantity = quantity;
        this._id = id;
        this._type = type;
        this._qtlimit = qtlimit;
    }

    get date() {
        return this._date;
    }

    get label() {
        return this._label;
    }

    getLabel() {
        return this._label;
    }

    getDateShort() {
        let day = this._date.getDate();
        let month = this._date.getMonth() + 1;

        if (day < 10) {
            day = "0" + day;
        }

        if (month < 10) {
            month = "0" + month;
        }

        return day + "/" + month + "/" + this._date.getFullYear().toString().slice(2);
    }

    getDatePythonFormat() {

        let day = this._date.getDate();
        let month = this._date.getMonth() + 1;
        let h = this._date.getHours();

        let m = this._date.getMinutes();

        if (day < 10) {
            day = "0" + day;
        }

        if (month < 10) {
            month = "0" + month;
        }

        if (h < 10) {
            h = "0" + h;
        }
        if (m < 10) {
            m = "0" + m;
        }

        return month + "/" + day + "/" + this._date.getFullYear() + ", " + h + ":" + m;

    }

    getId() {
        return this._id;
    }

    getType() {
        return this._type;
    }

    getQtlimit() {
        return this._qtlimit;
    }

    getShortYear() {
        return this._date.getFullYear().toString().slice(2);
    }

    getTimeString() {

        let h = this._date.getHours();

        let minutes = this._date.getMinutes();
        let timeAffix;
        let hours;

        if (minutes < 30) {
            minutes = "00";
        }


        if (h >= 12) {
            timeAffix = "PM";
        } else {
            timeAffix = "AM";
        }

        if (timeAffix == "AM") {
            hours = h;
        } else {
            hours = h % 12;
        }

        return ("" + hours + ":" + minutes + timeAffix);


    }

    getDateString() {
        let dayOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        let MonthOfYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];


        let day = dayOfWeek[this._date.getDay()];
        let month = MonthOfYear[this._date.getMonth()];


        return (day + ", " + month + " " + this._date.getDate());
    }

    getDayShortFormat() {
        let dayOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        let day = dayOfWeek[this._date.getDay()]
        return day;
    }

    get quantity() {
        return this._quantity;
    }


}


//Module for workouts tab
const ActivityCalendar = (() => {
    let calendar = [];

    function createButtonDiv(ses) {

        let button = document.createElement("button");
        button.classList.add("btn", "col", "p-2", "sessionBookingItem", "bg-white")
        button.setAttribute("data-bs-toggle", "modal");
        button.setAttribute("data-bs-target", "#book-workout")

        let activityLabel = "" // for custom labels given activity
        let textWrap = "text-nowrap"
        if (ses.getType() === "parking") {
            activityLabel = "Stall " + ses.getLabel()
        } else if (ses.getType() === "tennis") {
            textWrap = ""
            activityLabel = "Court " + ses.getLabel() + " " + ses.getTimeString()
        } else if (ses.getType() === "party") {
            // activityLabel = "Room " + ses.getLabel()

            activityLabel = ses.getLabel()
        } else {
            activityLabel = ses.getLabel()
        }
        let statusCont = ""
        let statusClass = ""
        if (ses.quantity === 0) {
            statusCont = "Available"
            statusClass = "bg-success text-white"
        } else if (ses.quantity >= 1) {
            statusCont = "Full"
            statusClass = "bg-danger text-white"
            //disable modal
            button.setAttribute("data-bs-toggle", "")
            button.setAttribute("data-bs-target", "")
        } else {
            statusClass = "bg-success text-white"
        }
        button.innerHTML = `
              <div class="row row-cols-2 g-1 p-1 border bg-light" sday="${ses.date.getDate()}" 
              smonth="${ses.date.getMonth() + 1}" syear="${ses.getShortYear()}" shour="${ses.date.getHours()}" 
              smin="${ses.date.getMinutes()}" sdateshort="${ses.getDateShort()}" sdatestring="${ses.getDateString()}" 
              sdatepythonformat="${ses.getDatePythonFormat()}" activityid="${ses.getId()}">
              <div class="col-7 fs-5 align-self-center ${textWrap}" >
                  ${activityLabel}
              </div>
              <div class="col-5 border rounded align-self-center text-white ${statusClass}">${statusCont}</div>
            </div>`


        return button
    }

    let fetchCalendar = () => {

        try {
            //placeholder fetch
            console.log(data);

            //creating some placeholders workouts sessions booked
            // workouts.push(new Workout(new Date(2021, 06, 17, 11, 30),50001, "ok"));

            //create 7 arrays, one for each day of the next 7 days
            //Then each day has 24 spots
            // calendar = data.forEach(d => {
            //   return new Activity(new Date(d.year, d.month - 1, d.day, d.hour, d.minute), d.count, d.label)
            // })


            let counter = 0;
            for (i = 0; i < 7; i++) {
                calendar.push([]);
                for (j = 0; j < data.length / 7; j++) {
                    let d = data[counter];
                    calendar[i].push(new Activity(new Date(d.year, d.month - 1, d.day, d.hour, d.minute), d.count, d.label, d.id, d.type, d.qtlimit));
                    counter++;
                }
            }
            console.log(calendar);


            //if nothing is pushed to workouts, don't populate
            if (calendar.length != 0) {
                console.log("received sessions");
                //update workouts
                _createActivitySessions(0);
                //populate the footer 7 days buttons
                _populateFooterButtons();
                //disable loaders
                _changeLoaders(true);
                //createEventListeners
                _createItemEventListener();
                _createFooterItemEventListener();


            } else {
                //if errors or no workouts do something with loaders
                _changeLoaders(false);
            }


        } catch (err) {
            console.log(err);
            console.log("something went wrong during the fetching of sessions");
            _changeLoaders(false);
        }
        //do the fetching


    }

    let _createActivitySessions = (day) => {
        //day is so we know which day session array we are taking from calendar
        let bookOnDate = document.getElementById("bookOnDate");
        let leftSlots = document.getElementById("leftslots");
        let rightSlots = document.getElementById("rightslots");

        calendar[day].forEach((ses, i) => {
            //set title header
            if (i == 0) {
                bookOnDate.textContent = ses.getDateString();
            }
            let but = createButtonDiv(ses)
            if (i % 4 === 0 || i % 4 === 1) {
                leftSlots.append(but)
            } else {
                rightSlots.append(but)
            }
        })

        //create new Item Event Listeners
        _createItemEventListener();
    }

    let _populateFooterButtons = () => {
        let footerButtonsContainer = document.getElementById("footerButtonsContainer");

        //structure
        // <div class="col">
        //   <button class="btn btn-primary fs-5 fw-bold text-center footerButton">
        //     Mon<br>
        //     <span id="monAvailability">60%</span>
        //   </button>
        // </div>
        calendar.forEach((week, index) => {
            let div = document.createElement("div");
            div.classList.add("col", "p-0");

            let day = week[0].getDayShortFormat();

            let p = document.createElement("p");
            p.classList.add("mb-0");
            p.innerText = day
            let button = document.createElement("button");
            button.classList.add("btn", "btn-outline-primary", "fs-6", "text-center", "footerButton", "fw-light");

            button.append(p)

            let span = document.createElement("span");


            let availability = 0;
            let counter = 0;


            week.forEach(ses => {
                availability += ses.quantity;
                counter++;
            })

            let quantity_limit = week[0].getQtlimit();

            let percentage = (availability / (counter * quantity_limit)) * 100;

            span.textContent = parseFloat(percentage).toFixed(2) + "%";

            button.setAttribute("weekIndex", index);
            button.append(span);
            div.append(button);
            footerButtonsContainer.append(div);

        })


    }

    let _createFooterItemEventListener = () => {
        let buttons = document.querySelectorAll(".footerButton");

        buttons.forEach(b => {
            b.addEventListener("click", () => {
                document.getElementById("leftslots").innerHTML = ""
                document.getElementById("rightslots").innerHTML = ""

                _createActivitySessions(b.getAttribute("weekIndex"));

                _changeLoaders(true);
            })

        })


    }


    let _createItemEventListener = () => {
        //get all the upcomingWorkoutList
        let sessionBookingItem = document.querySelectorAll(".sessionBookingItem");

        //set event Listeners
        //when user clicks an upcoming workout we
        sessionBookingItem.forEach((el, index) => {
            el.addEventListener("click", (e) => {
                _populateBookingModal(el);

            })
        })
    }

    let _populateBookingModal = (el) => {
        let modalTime = document.getElementById("modalTime");
        let modalDate = document.getElementById("modalShortDate");
        let modalDateString = document.getElementById("modalDateString");
        let timeStampPost = document.getElementById("timeStampPost");
        let activityId = document.getElementById("activityId")

        //structure of element
        // <button class="list-group-item list-group-item-action d-flex px-2 sessionBookingItem"
        // data-bs-toggle="modal" data-bs-target="#book-workout">
        //     <div class="fs-5 align-items-center w-50" bDay="" bMonth="" bYear="" bHour="" bMin="" bDateShort="25/08/21">06:00AM</div>
        //     <div class="bg-success text-white border rounded primary row row-cols-2 flex-grow-1 mx-2 align-items-center justify-content-center">0/4</div>
        // </button>
        modalTime.textContent = el.children[0].children[0].textContent;
        modalDate.textContent = el.children[0].getAttribute("sDateShort");
        modalDateString.textContent = el.children[0].getAttribute("sDateString");
        timeStampPost.setAttribute("value", el.children[0].getAttribute("sDatePythonFormat"));
        activityId.setAttribute("value", el.children[0].getAttribute("activityId"))


    }


    let _changeLoaders = (success) => {
        let loader = document.getElementById("loader");
        let weeksLoader = document.getElementById("weeksLoader");


        if (success) {
            console.log("success loading activity calendar")
            loader.style.display = "none";
            weeksLoader.style.display = "none";
        } else {
            console.log("fail loading activity calendar")
            loader.textContent = "No Activity found!";
            weeksLoader.textContent = "No Schedule found!";
        }

    }


    return {fetchCalendar}
})();


//create event listeners;
window.onload = ActivityCalendar.fetchCalendar();




