

document.addEventListener("DOMContentLoaded", () =>{

    // get user id from django
    const id = JSON.parse(document.getElementById('user_id').textContent)
    let start = 0;
    let amount = 5;

    function display(data) {
        data["posts"].forEach(post => {
            const post_div = document.createElement('div');
            post_div.className = 'post';
            const owner_div = document.createElement('div');
            owner_div.className = 'owner';
            const text_div = document.createElement('div');
            text_div.className = 'text';
            const like_div = document.createElement('div');
            like_div.className = 'like';
            const com_div = document.createElement('div');
            com_div.className = 'com';
            const date_div = document.createElement('div');
            date_div.className = 'date';
            const edit_div = document.createElement('div');
            edit_div.className = 'edit';

            text_div.innerHTML = post.text;
            owner_div.innerHTML = `<a href=\"${post.owner.id}\">${post.owner.username}</a>`;
            like_div.innerHTML = `<i class=\"bi-hand-thumbs-up\" style=\"font-size: 1.8rem;\"></i> ${post.likes}`;
            com_div.innerHTML = "<a>comments</a>";
            date_div.innerHTML = post.timestamp.toString().split('T')[0];

            post_div.append(owner_div);
            post_div.append(text_div);
            post_div.append(date_div);
            post_div.append(like_div);
            post_div.append(com_div);
            document.querySelector("#all_posts").append(post_div);
        })
        start += amount + 1;
    }


    newMails()

    function newMails(){
        fetch(`posts?start=${start}&end=${start + amount}&owner=${id}`)
            .then(response => response.json())
            .then(data => {
                display(data);
                });
    }

    let is_fetching = false;

    window.onscroll = () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight){
            if (!is_fetching) {
                is_fetching = true;
                console.log('start')
                newMails();
            } else {
            is_fetching = false;
        }}
}
})
