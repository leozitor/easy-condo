//All methods and calls are at the end


//create usage to post the booked session

class Activity {
    constructor(date, quantity, label){
        this._date = date;
        this._label = label
        this._quantity = quantity;
    }

    get date(){
        return this._date;
    }

    get label(){
        return this._label;
    }

    getLabel(){
        return this._label;
    }

    getDateShort(){
        let day = this._date.getDate();
        let month = this._date.getMonth() + 1;

        if(day < 10){
            day = "0" + day;
        }

        if(month < 10){
            month = "0" + month;
        }

        return day + "/" + month + "/" + this._date.getFullYear().toString().slice(2);
    }

    getDatePythonFormat(){

        let day = this._date.getDate();
        let month = this._date.getMonth() + 1;
        let h = this._date.getHours();

        let m = this._date.getMinutes();

        if(day < 10){
            day = "0" + day;
        }

        if(month < 10){
            month = "0" + month;
        }

        if(h <10){
            h = "0"+h;
        }
        if(m<10){
            m = "0"+m;
        }

        return month + "/" + day + "/" + this._date.getFullYear() + ", " + h + ":" + m;

    }

    getShortYear(){
        return this._date.getFullYear().toString().slice(2);
    }

    getTimeString(){

        let h = this._date.getHours();

        let minutes = this._date.getMinutes();
        let timeAffix;
        let hours;

        if(minutes < 30){
            minutes = "00";
        }


        if(h >= 12){
            timeAffix = "PM";
        }else{
            timeAffix = "AM";
        }

        if(timeAffix == "AM"){
            hours = h;
        }else{
            hours = h%12;
        }

        return ("" + hours + ":" + minutes + timeAffix);


    }

    getDateString(){
        let dayOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        let MonthOfYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];



        let day = dayOfWeek[this._date.getDay()];
        let month = MonthOfYear[this._date.getMonth()];


        return (day + ", " + month + " " + this._date.getDate() );
    }

    getDayShortFormat(){
        let dayOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        let day = dayOfWeek[this._date.getDay()]
        return day;
    }

    get quantity(){
        return this._quantity;
    }



}




//Module for workouts tab
const ActivityCalendar  = (()=>{
    let calendar = [];


    let fetchCalendar = () =>{

        try{
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
            for(i = 0; i < 7; i++){
                calendar.push([]);
                for(j=0; j<data.length/7; j++){
                    let d = data[counter];
                    calendar[i].push(new Activity(new Date(d.year, d.month - 1, d.day, d.hour, d.minute), d.count, d.label));
                    counter++;
                }
            }
            console.log(calendar);





            //if nothing is pushed to workouts, don't populate
            if(calendar.length != 0){
                console.log("received sessions");
                //update workouts
                createActivitySessions(0);
                //populate the footer 7 days buttons
                _populateFooterButtons();
                //disable loaders
                _changeLoaders(true);
                //createEventListeners
                _createItemEventListener();
                _createFooterItemEventListener();


            }else{
                //if errors or no workouts do something with loaders
                _changeLoaders(false);
            }




        } catch(err){
            console.log(err);
            console.log("something went wrong during the fetching of sessions");
            _changeLoaders(false);
        }
        //do the fetching



    }

    let createActivitySessions = (day) =>{
        //day is so we know which day session array we are taking from calendar
        let bookOnDate = document.getElementById("bookOnDate");
        let slots = document.getElementById("slots");

        let newFlexDiv;
        calendar[day].forEach((ses,i)=>{
            //set title header
            if(i == 0){
                bookOnDate.textContent = ses.getDateString();
            }

            // <div class="d-flex">
            // <button class="list-group-item list-group-item-action d-flex px-2 sessionBookingItem"
            // data-bs-toggle="modal" data-bs-target="#book-workout">
            //   <div class="fs-5 align-items-center w-50" sDay="" sMonth="" sYear="" sHour="" sMin="" sDateShort="25/08/21">06:00AM</div>
            //   <div class="bg-success text-white border rounded primary row row-cols-2 flex-grow-1 mx-2 align-items-center justify-content-center">0/4</div>
            // </button>*2
            //</div>

            // <div className="container d-flex flex-wrap px-4 py-2">
            //     <!-- slots -->
            //     <button className="row px-2 sessionBookingItem d-flex" data-bs-toggle="" data-bs-target="">
            //         <div className="col fs-5" sday="7" smonth="3" syear="22" shour="0" smin="0"
            //              sdateshort="07/03/22" sdatestring="Monday, March 7" sdatepythonformat="03/07/2022, 00:00">stall
            //             1
            //         </div>
            //         <div className=" col border rounded bg-success text-white align-self-center bg-white">available
            //         </div>
            //     </button>
            //
            //
            // </div>
            let button = document.createElement("button");
            button.classList.add("row","ms-0", "me-2", "p-2", "border","sessionBookingItem", "bg-white");
            button.setAttribute("data-bs-toggle", "modal");
            button.setAttribute("data-bs-target", "#book-workout");

            let firstDiv = document.createElement("div");
            firstDiv.classList.add("col", "fs-5", "align-self-center");
            firstDiv.setAttribute("sDay", ses.date.getDate());
            firstDiv.setAttribute("sMonth", ses.date.getMonth()+1);
            firstDiv.setAttribute("sYear", ses.getShortYear());
            firstDiv.setAttribute("sHour", ses.date.getHours());
            firstDiv.setAttribute("sMin", ses.date.getMinutes());
            firstDiv.setAttribute("sDateShort", ses.getDateShort());
            firstDiv.setAttribute("sDateString", ses.getDateString());
            firstDiv.setAttribute("sDatePythonFormat", ses.getDatePythonFormat());
            firstDiv.textContent = ses.getLabel();

            button.append(firstDiv);

            let secondDiv = document.createElement("div");
            secondDiv.classList.add("col", "border", "rounded", "align-self-center");
            if(ses.quantity ==0){
                secondDiv.textContent = "available"
                secondDiv.classList.add("bg-success", "text-white");
                //disable modal
                button.setAttribute("data-bs-toggle", "");
                button.setAttribute("data-bs-target", "");
            }
            else if(ses.quantity >= 1){
                secondDiv.textContent = "Full"
                secondDiv.classList.add("bg-danger", "text-white");
                //disable modal
                button.setAttribute("data-bs-toggle", "");
                button.setAttribute("data-bs-target", "");
            }else{
                secondDiv.classList.add("bg-success", "text-white");
            }

            button.append(secondDiv);
            //end of div or start of div
            slots.append(button);
        })

        //create new Item Event Listeners
        _createItemEventListener();
    }

    let _populateFooterButtons = ()=>{
        let footerButtonsContainer = document.getElementById("footerButtonsContainer");

        //structure
        // <div class="col">
        //   <button class="btn btn-primary fs-5 fw-bold text-center footerButton">
        //     Mon<br>
        //     <span id="monAvailability">60%</span>
        //   </button>
        // </div>
        calendar.forEach((week,index)=>{
            let div = document.createElement("div");
            div.classList.add("col");

            let day = week[0].getDayShortFormat();

            let button = document.createElement("button");
            button.classList.add("btn", "btn-primary", "fs-5", "fw-bold", "text-center", "footerButton");
            button.textContent = day;
            button.append(document.createElement("br"));

            let span = document.createElement("span");

            let availability = 0;
            let counter = 0;


            week.forEach(ses=>{
                availability += ses.quantity;
                counter++;
            })


            let percentage = (availability / (counter*4))*100;

            span.textContent = parseFloat(percentage).toFixed(2)+"%";

            button.setAttribute("weekIndex", index);
            button.append(span);
            div.append(button);
            footerButtonsContainer.append(div);

        })



    }

    let _createFooterItemEventListener=()=>{
        let buttons = document.querySelectorAll(".footerButton");

        buttons.forEach(b=>{
            b.addEventListener("click", ()=>{
                let slots = document.getElementById("slots");

                slots.innerHTML = "";

                let loader = document.createElement("div");
                loader.setAttribute("id", "loader");
                loader.textContent = "Loading..."
                slots.append(loader);

                createActivitySessions(b.getAttribute("weekIndex"));

                _changeLoaders(true);
            })

        })



    }


    let _createItemEventListener = () =>{
        //get all the upcomingWorkoutList
        let sessionBookingItem = document.querySelectorAll(".sessionBookingItem");

        //set event Listeners
        //when user clicks an upcoming workout we
        sessionBookingItem.forEach((el,index)=>{
            el.addEventListener("click", (e) =>{
                _populateBookingModal(el);

            })
        })
    }

    let _populateBookingModal =(el)=>{
        let modalTime = document.getElementById("modalTime");
        let modalDate = document.getElementById("modalShortDate");
        let modalDateString = document.getElementById("modalDateString");
        let timeStampPost = document.getElementById("timeStampPost");

        //structure of element
        // <button class="list-group-item list-group-item-action d-flex px-2 sessionBookingItem"
        // data-bs-toggle="modal" data-bs-target="#book-workout">
        //     <div class="fs-5 align-items-center w-50" bDay="" bMonth="" bYear="" bHour="" bMin="" bDateShort="25/08/21">06:00AM</div>
        //     <div class="bg-success text-white border rounded primary row row-cols-2 flex-grow-1 mx-2 align-items-center justify-content-center">0/4</div>
        // </button>

        modalTime.textContent = el.children[0].textContent;
        modalDate.textContent = el.children[0].getAttribute("sDateShort");
        modalDateString.textContent = el.children[0].getAttribute("sDateString");
        timeStampPost.setAttribute("value", el.children[0].getAttribute("sDatePythonFormat"));




    }


    let _changeLoaders = (success)=>{
        let loader = document.getElementById("loader");
        let weeksLoader = document.getElementById("weeksLoader");


        if(success){
            loader.style.display = "none";
            weeksLoader.style.display = "none";
        }else{
            loader.textContent = "No Activity found!";
            weeksLoader.textContent = "No Schedule found!";
        }

    }


    return {fetchCalendar}
})();


//create event listeners;
window.onload = ActivityCalendar.fetchCalendar();




