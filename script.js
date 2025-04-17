
function isDateInAnyRange(dateStr, ranges) {
    const date = new Date(dateStr);
    return ranges.some(([start, end]) => {
        const startDate = new Date(start);
        const endDate = new Date(end);
        return date >= startDate && date <= endDate;
    });
}



function calculateAttendance(data, courses, medicals,username) {
    const output = document.getElementById('progress-container');
    console.log("Data:", medicals);
    const tg = document.createElement('h3');
    tg.className = "username";
    tg.textContent = `${username}`;
    output.appendChild(tg);

    let count = 0;
    for (const course in data) {
        console.log(course);
        let progresscard = document.createElement('div');
        progresscard.className = "progress-card";
       
        const courseTitle = document.createElement('h4');
        courseTitle.className = "course-title";
        courseTitle.textContent = `${courses[count][0]}  ${courses[count][1]}`;
        output.appendChild(progresscard);
        progresscard.appendChild(courseTitle);
        let progressBar = document.createElement('div');
        progressBar.className = "progress-bar-container";
        output.appendChild(progressBar);
        let elem = document.createElement('div');
        elem.className = "progress-bar";


        let present = 0;
        let absent = 0;
        let medical = 0;

        data[course].forEach(([lid, date, hours, type, time, group, status]) => {


            if (status === "Present") {
                present += parseFloat(hours);
            } else if (status === "Absent") {

                if (medicals.length > 0) {
                    console.log("Medical Date Found")
                    if (isDateInAnyRange(date, medicals)) {
                        console.log("Medical Date Found")
                        medical += parseFloat(hours);
                    } else {
                        absent += parseFloat(hours);
                    }

                } else {
                    absent += parseFloat(hours);
                }

            }

        });
        console.log("Present:", present);
        console.log("Absent:", absent);
        console.log("Medical:", medical);


        const total = present + absent + medical;
        let meidcalBar = document.createElement('div');
        if (medical != 0) {

            meidcalBar.className = "progress-bar-medical";
            meidcalBar.style.width = (medical / total) * 100 + "%";

        }

        const percentage = total === 0 ? 0 : ((present + medical) / total) * 100;
        const presentPercentage = (present / total) * 100;



        if (presentPercentage < 80) {
            elem.style.backgroundColor = "red";
        }

        elem.style.width = presentPercentage + "%";
        let textContent = document.createElement('span');
        textContent.className = "progress-text";
        textContent.innerHTML = `${percentage.toFixed(1)}%`;
        elem.appendChild(textContent);
        progressBar.appendChild(elem);

        if (medical != 0) {
            progressBar.appendChild(meidcalBar);
        }
        progresscard.appendChild(progressBar);
        count++;
    }
}



fetch("courses.json")
    .then(response => response.json())
    .then(courses => {
        console.log(courses);



        fetch("./attendance_data.json")
            .then(response => response.json())
            .then(data => {
                console.log(data);


                if (courses.length == Object.keys(data).length) {
                    console.log("Length is equal")


                    //medical check

                    fetch("medicals.json")
                        .then(response => response.json())
                        .then(medicals => {
                            console.log("meical loaded:", medicals);


                            fetch("username.json")
                                .then(response => response.json())
                                .then(username => {
                                    console.log("username loaded:", username);


                                    calculateAttendance(data, courses, medicals, username);
                                })
                                .catch(error => {
                                    console.error('Error loading  username JSON:', error);
                                });

                        })
                        .catch(error => {
                            console.error('Error loading  meical JSON:', error);
                        });




                    const output = document.getElementById('output');


                    for (const course in data) {
                        const courseTitle = document.createElement('h2');
                        courseTitle.textContent = course;
                        output.appendChild(courseTitle);

                        const table = document.createElement('table');
                        table.border = "1";
                        data[course].forEach(([lid, date, hours, type, time, group, status]) => {
                            const row = document.createElement('tr');

                            const dateCell = document.createElement('td');
                            dateCell.textContent = date;
                            row.appendChild(dateCell);

                            const hoursCell = document.createElement('td');
                            hoursCell.textContent = hours;
                            row.appendChild(hoursCell);

                            const typeCell = document.createElement('td');
                            typeCell.textContent = type;
                            row.appendChild(typeCell);

                            const timeCell = document.createElement('td');
                            timeCell.textContent = time;
                            row.appendChild(timeCell);

                            const statusCell = document.createElement('td');
                            statusCell.textContent = status;
                            row.appendChild(statusCell);

                            table.appendChild(row);
                        });
                        output.appendChild(table);
                    }





                }
                else {
                    console.log("Length is not equal")
                    const output = document.getElementById('output');
                    const errorMessage = document.createElement('h2');
                    errorMessage.textContent = "Error: Length of courses and attendance data do not match.";
                    output.appendChild(errorMessage);

                }



            })
            .catch(error => {
                console.error('Error loading data JSON:', error);
            });


    })
    .catch(error => {
        console.error('Error course loading JSON:', error);
    });

