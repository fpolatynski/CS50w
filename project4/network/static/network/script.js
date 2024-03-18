
// When DOM content is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add onsubmit function
    document.querySelector('#asd').onclick = () =>{
        const text = document.querySelector("#new_post-text").value;
        fetch("/new_post", {
            method: 'POST',
            body: JSON.stringify({
                text: text
            })
        })
        document.querySelector("#new_post-text").value = "";
    }
});
