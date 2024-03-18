document.addEventListener('DOMContentLoaded', () => {

    // Query all buttons and add onclick function
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            // Change all divs display to none
            document.querySelectorAll('div').forEach(div => {
                div.style.display = 'none';
            });
            // Change button clicked visibility to block
            document.querySelector(`#${button.dataset.page}`).style.display = 'block';
        }
    });

});