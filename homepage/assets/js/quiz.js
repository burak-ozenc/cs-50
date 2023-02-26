// logic for checking answers
window.onload = function () {
    document.getElementById('check').addEventListener('click', () => {

        // check if user give answer to all questions
        let isValid = validateCheck()

        // if valid
        // start checking process
        // else alert
        if (isValid == true) {
            handleCheck()
        } else {
            alert('Some fields are empty')
        }
    })
}

// check if user give answer to all questions
// else alert
function validateCheck() {
    for (let i = 1; i < 6; i++) {
        // for every question
        // if both element unchecked return false
        let first = document.getElementById(`q${i}-true`)
        let second = document.getElementById(`q${i}-false`)
        if (first.checked == false && second.checked == false) {
            return false
        }
    }
    return true
}


// for validating
// get element and check if the correct answer selected
// print the input correct or incorrect
// style the answer
function handleCheck() {
    let q1 = document.getElementById('q1-false')
    let answer1 = document.getElementById("answer-1")

    if (q1.checked == true) {
        answer1.innerHTML = "Correct!"
        q1.labels[0].style.color = "green"
        q1.labels[0].style.fontWeight = "700"
    } else {
        let q1False = document.getElementById('q1-true')
        answer1.innerHTML = "Incorrect!"
        q1False.labels[0].style.color = "red"
        q1False.labels[0].style.fontWeight = "700"
    }


    let q2 = document.getElementById('q2-true')
    let answer2 = document.getElementById("answer-2")

    if (q2.checked == true) {
        answer1.innerHTML = "Correct!"
        q2.labels[0].style.color = "green"
        q2.labels[0].style.fontWeight = "700"
    } else {
        let q2False = document.getElementById('q2-false')
        answer2.innerHTML = "Incorrect!"
        q2False.labels[0].style.color = "red"
        q2False.labels[0].style.fontWeight = "700"
    }


    let q3 = document.getElementById('q3-true')
    let answer3 = document.getElementById("answer-3")

    if (q3.checked == true) {
        answer3.innerHTML = "Correct!"
        q3.labels[0].style.color = "green"
        q3.labels[0].style.fontWeight = "700"
    } else {
        let q3False = document.getElementById('q3-false')
        answer3.innerHTML = "Incorrect!"
        q3False.labels[0].style.color = "red"
        q3False.labels[0].style.fontWeight = "700"
    }


    let q4 = document.getElementById('q4-false')
    let answer4 = document.getElementById("answer-4")

    if (q4.checked == true) {
        answer4.innerHTML = "Correct!"
        q4.labels[0].style.color = "green"
        q2.labels[0].style.fontWeight = "700"
    } else {
        let q4False = document.getElementById('q4-true')
        answer4.innerHTML = "Incorrect!"
        q4False.labels[0].style.color = "red"
        q4False.labels[0].style.fontWeight = "700"
    }


    let q5 = document.getElementById('q5-false')
    let answer5 = document.getElementById("answer-5")

    if (q5.checked == true) {
        answer5.innerHTML = "Correct!"
        q5.labels[0].style.color = "green"
        q2.labels[0].style.fontWeight = "700"
    } else {
        let q5False = document.getElementById('q5-true')
        answer5.innerHTML = "Incorrect!"
        q5False.labels[0].style.color = "red"
        q5False.labels[0].style.fontWeight = "700"
    }

}