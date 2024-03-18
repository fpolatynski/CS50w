
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
    newMails()
});

let start = 0;
let amount = 5;

function display(data){
    data["posts"].forEach(post => {
        const post_div = document.createElement('div')
        post_div.className = 'post'
        const owner_div = document.createElement('div')
        owner_div.className = 'owner'
        const text_div = document.createElement('div')
        text_div.className = 'text'

        text_div.innerHTML = post.text
        owner_div.innerHTML = post.owner;
        post_div.append(owner_div)
        post_div.append(text_div)
        document.querySelector("#all_posts").append(post_div)
    })
    start += amount;
}

function newMails(){
    fetch(`posts?start=${start}&end=${start + amount}`)
        .then(response => response.json())
        .then(data => {
            display(data)
            });
}

