if (!localStorage.getItem('temp')){
    localStorage.setItem('temp', 0);
}
function plus() {
    let temp = localStorage.getItem('temp')
    temp ++;
    document.querySelector("h1").innerHTML = temp;
    localStorage.setItem('temp', temp)
    if (temp % 10 === 0) {
        alert(`Count is ${temp}`);
    }
}
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("h1").innerHTML = localStorage.getItem('temp')
    document.querySelector('button').onclick = plus;

    //setInterval(plus, 1000);

});