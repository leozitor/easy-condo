//All methods and calls are at the end


//update the deleteWorkoutEventListener to do a post.


class Workout{
    constructor(date, id, status){
        this._date = date;
        this._id = id;

        //status can be Booked, Missed, Canceled
        this._status = status;
    }

    get date(){
        return this._date;
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

        let day = dayOfWeek[this._date.getDay()]


        return (day + ", " + this._date.getDate() + " at ");
    }

    get id(){
        return this._id;
    }

    get status(){
        return this._status;
    }

    

}




//Module for workouts tab
const userDash  = (()=>{
    let workouts = [];

    let _createUpcomingWorkoutList = () =>{
        //upcoming
        //lets filter workouts, we only want ones that are bigger than Date.now()
        let today = new Date();

        let upcomingBookings = workouts.filter(wo=>{
            return (wo.date.getTime() > today.getTime());
        })

        //sort in ascending order
        upcomingBookings.sort((a,b)=>{
           return a.date.getTime() - b.date.getTime();
        });

        _populateWorkoutTabUpcomingList(upcomingBookings);

        _populateDiaryTabUpcomingList(upcomingBookings);


        
        
    }

    let _createFinishedWorkoutList = () =>{
        let today = new Date();

        let finishedBookings = workouts.filter(wo=>{
            return (wo.date.getTime() < today.getTime());
        })

        //sort in descending order
        finishedBookings.sort((a,b)=>{
            return b.date.getTime() - a.date.getTime();
        });

        let workoutDiaryTabFinishedList = document.getElementById("workoutDiaryTabFinishedList");

        //structure, if missed or canceled add to div bg-danger, bg-gradient, text-white.
        // <div class="list-group-item list-group-item-action ">
        //     <div class="d-flex w-100 justify-content-between">
        //         <h5 class="mb-1">25/08/21 - 10:00AM</h5>
        //     </div>
        //     <small class="text-muted">id:3456789</small>
        // </div>

        finishedBookings.forEach(wo=>{


            let divList = document.createElement("div");
            divList.classList.add("list-group-item", "list-group-item-action");
            if(wo.status == "Missed"){
                divList.classList.add("bg-danger", "bg-gradient", "text.white");
            }else if(wo.status == "Canceled"){
                divList.classList.add("bg-warning", "bg-gradient");
            }

            let divTitle = document.createElement("div");
            divTitle.classList.add("d-flex", "w-100", "justify-content-between");

            let hDate = document.createElement("h5");
            hDate.classList.add("mb-1");
            hDate.textContent = wo.getDateShort() + " - " + wo.getTimeString();

            divTitle.append(hDate);

            let smallId = document.createElement("small");
            smallId.classList.add("text-muted");
            smallId.textContent = "id: " + wo.id;

            divList.append(divTitle);
            divList.append(smallId);

            workoutDiaryTabFinishedList.append(divList);
        })


    }

    let _createWorkoutStats = () =>{
        let remainingTrainings = document.getElementById("remainingTrainings");
        let finishedTrainings = document.getElementById("finishedTrainings");
        let missedTrainings = document.getElementById("missedTrainings");
        let totalTimeGym = document.getElementById("totalTimeGym");

        let today = new Date();
        let remainingBookings = workouts.filter(wo=>{
            return ((wo.date.getTime() > today.getTime()) && wo.status == "Booked");
        })

        let finishedBookings = workouts.filter(wo=>{
            return (wo.date.getTime() < today.getTime());
        })

        let finishedOkBookings = finishedBookings.filter(wo=>{
            return(wo.status == "Booked")
        });

        finishedTrainings.textContent = finishedOkBookings.length;

        missedTrainings.textContent = finishedBookings.filter(wo=>{
            return(wo.status == "Missed")
        }).length;

        remainingTrainings.textContent = remainingBookings.length;

        let gymTimeHours = Math.floor(finishedOkBookings.length / 2);
        let gymTimeMinutes = finishedOkBookings.length % 2;
        if(gymTimeMinutes == 1){
            gymTimeMinutes = 30;
        }

        totalTimeGym.textContent = gymTimeHours + "h" + gymTimeMinutes + "m";






    }

    let _populateDiaryTabUpcomingList = (upcomingBookings) =>{
        //Workout Diary Tab
        let workoutDiaryUpcomingTabList = document.getElementById("workoutDiaryUpcomingTabList");

        //structure 
        // <div class="list-group-item list-group-item-action ">
        //     <div class="d-flex w-100 justify-content-between">
        //         <h5 class="mb-1">25/08/21 - 10:00AM</h5>
        //     </div>
        //     <small class="text-muted">id:3456789</small>
        // </div>

        upcomingBookings.forEach(wo=>{
            if(wo.status != "Booked"){
                return;
            }

            let divList = document.createElement("div");
            divList.classList.add("list-group-item", "list-group-item-action");

            let divTitle = document.createElement("div");
            divTitle.classList.add("d-flex", "w-100", "justify-content-between");

            let hDate = document.createElement("h5");
            hDate.classList.add("mb-1");
            hDate.textContent = wo.getDateShort() + " - " + wo.getTimeString();

            divTitle.append(hDate);

            let smallId = document.createElement("small");
            smallId.classList.add("text-muted");
            smallId.textContent = "id: " + wo.id;

            divList.append(divTitle);
            divList.append(smallId);

            workoutDiaryUpcomingTabList.append(divList);

        })
    }


    let _populateWorkoutTabUpcomingList = (upcomingBookings) =>{
        //Workout Tab
        let workoutTabList = document.getElementById("mainWorkoutTabList");
        //Structure we are looking for ==
        // <button class="list-group-item list-group-item-action upcomingWorkoutItem">
        //         <div class="d-flex w-100 justify-content-between">
        //           <h5 class="mb-1">Monday, 25th at <span class="item-time-span">10:00AM</span></h5>
        //         </div>
        //         <p class="mb-1">25/08/21</p>
        //         <small class="text-muted">id:<span>3456789</span></small>
        //       </button>

        upcomingBookings.forEach((wo, index)=>{
            if(wo.status != "Booked"){
                return;
            }

            let button = document.createElement("button");
            button.classList.add("list-group-item", "list-group-item-action", "upcomingWorkoutItem");

            let divTitle = document.createElement("div");
            divTitle.classList.add("d-flex", "w-100", "justify-content-between");

            let dateHeader = document.createElement("h5");
            dateHeader.classList.add("mb-1");
            dateHeader.textContent = wo.getDateString();

            let timeSpan = document.createElement("span");
            timeSpan.classList.add("item-time-span");
            timeSpan.textContent = wo.getTimeString();

            dateHeader.append(timeSpan);
            divTitle.append(dateHeader);

            let dateShortFormat = document.createElement("p");
            dateShortFormat.classList.add("mb-1");
            dateShortFormat.textContent = wo.getDateShort();

            let idHolder = document.createElement("small");
            idHolder.classList.add("text-muted");
            idHolder.textContent = "id: ";

            let spanId = document.createElement("span");
            spanId.textContent = wo.id;

            idHolder.append(spanId);

            button.append(divTitle);
            button.append(dateShortFormat);
            button.append(idHolder);

            workoutTabList.append(button);

            //populate main tab and modal
            if(index == 0){
                _populateMainAndModal(button);
            }

        });
    }

    let _changeLoaders = (success)=>{
        let mainTabLoader = document.getElementById("mainWorkoutTabLoader");
        let diaryWorkoutTabLoader = document.getElementById("diaryWorkoutTabLoader");
        let diaryFinishedTabLoader = document.getElementById("diaryFinishedTabLoader");

        if(success){
            mainTabLoader.style.display = "none";
            diaryWorkoutTabLoader.style.display = "none";
            diaryFinishedTabLoader.style.display = "none";
        }else{
            mainTabLoader.textContent = "No Scheduled Workouts found!";
            diaryWorkoutTabLoader.textContent = "No Scheduled Workouts found!";
            diaryFinishedTabLoader.textContent = "No Scheduled Workouts found!";
        }
        
    }

    let fetchWorkouts = async() =>{
            
        try{
            //get data from global scope
            console.log(data);
            //console.log(data.size);

            data.forEach(wo=>{
                workouts.push(new Workout(new Date(wo.year, wo.month - 1, wo.day, wo.hour, wo.minute),wo.id, "Booked"));
            })
            console.log(workouts);

            //creating some placeholders workouts sessions booked
            // workouts.push(new Workout(new Date(2021, 06, 17, 11, 30),50001, "ok"));
            // workouts.push(new Workout(new Date(2021, 06, 22, 18, 30),50001, "ok"));
            

            
            
            //if nothing is pushed to workouts, don't populate
            if(workouts.length != 0){
                console.log("user has workouts");
                //update workouts
                _createUpcomingWorkoutList();
                _createFinishedWorkoutList();
                _createWorkoutStats();
                //disable loaders
                _changeLoaders(true);


                //createEventListeners();
                _createItemEventListener();
                _cancelWorkoutEventListener();


            }else{
                //if errors or no workouts do something with loaders
                _changeLoaders(false);
            }
            

            

        } catch(err){
            console.log(err);
            console.log("something went wrong during the fetching of workouts")
        }
        //do the fetching

        

    }

    let _cancelWorkoutEventListener =() =>{
        let modalDelete = document.getElementById("modalWorkoutDeleteButton");

        modalDelete.addEventListener("click", (el)=>{
            //send a post Request with id
            let id = document.getElementById("modalWorkoutId").textContent;
            //_postWorkoutCancel(id);
            //ok, missed, canceled
        })
    }



    let _createItemEventListener = () =>{
        //get all the upcomingWorkoutList
        let upcomingWorkouts = document.querySelectorAll(".upcomingWorkoutItem");

        //set event Listeners
        //when user clicks an upcoming workout we
        upcomingWorkouts.forEach((el,index)=>{
            el.addEventListener("click", (e) =>{
                _populateMainAndModal(el)
            })
        })
    }

    let _populateMainAndModal = (el)=>{
        console.log("Extracting values for list item");
                //get title
                let title = el.children[0].children[0].textContent;
                //getting time
                let time = el.children[0].children[0].children[0].textContent;
                //get date
                let date = el.children[1].textContent;
                //get id
                let id = el.children[2].children[0].textContent;

                //populate main workout and Modal
                _populateMainWorkoutTabAndModal(title, time, date, id);
                _cancelWorkoutEventListener();
    }

    let _populateMainWorkoutTabAndModal = (title, time, date, id) =>{
        //get elements and assign new values, first main then modal
        document.getElementById("mainWorkoutTitle").textContent = title;
        document.getElementById("mainWorkoutTime").textContent = time;
        document.getElementById("mainWorkoutDate").textContent = date;
        document.getElementById("mainWorkoutId").textContent = id;
        //modal populate
        document.getElementById("modalWorkoutTime").textContent = time;
        document.getElementById("modalWorkoutDate").textContent = date;
        document.getElementById("modalWorkoutId").textContent = id;
        document.getElementById("idPost").setAttribute("value", id);

    }

    

    return {fetchWorkouts}
})();


//fetch

//create event listeners;
window.onload = userDash.fetchWorkouts();
