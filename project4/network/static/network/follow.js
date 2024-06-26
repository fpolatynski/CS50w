// When DOM content is loaded
document.addEventListener('DOMContentLoaded', () => {
    let page = 1;
    newMail();

    document.querySelector("#next").onclick = () => {
        page += 1;
        newMail();
    }

    document.querySelector("#previous").onclick = () => {
        if (page > 1){
            page -= 1;
            newMail();
        }
    }

    function newMail(){
        fetch(`posts?page=${page}&owner=f`)
            .then(response => response.json())
            .then(data => {
                display(data);
                });
        window.scrollTo(0, 0);
    }

    function display(data){
        document.querySelector("#all_posts").innerHTML = "";
        const user = data["current_user"];
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

            text_div.innerHTML = post.text.replaceAll("\n", "<br>");
            owner_div.innerHTML = `<a href=\"${post.owner.id}\">${post.owner.username}</a>`;
            com_div.innerHTML = "<a href=\"https://github.com/fpolatynski\">comments</a>";
            date_div.innerHTML = post.timestamp.toString().split('T')[0];

            post_div.append(owner_div);
            post_div.append(text_div);
            post_div.append(date_div);
            post_div.append(like_div);
            post_div.append(com_div);
            document.querySelector("#all_posts").append(post_div);
            if (post.likers.includes(user.id)) {
                like_div.innerHTML = `<i id=\"a${post.id}\" class=\"bi-hand-thumbs-up-fill\" style=\"font-size: 1.8rem;\"></i> ${post.likes}`;
            } else {
                like_div.innerHTML = `<i id=\"a${post.id}\" class=\"bi-hand-thumbs-up\" style=\"font-size: 1.8rem;\"></i> ${post.likes}`;
            }

            let emoji = document.querySelector(`#a${post.id}`);
            add_listiner(emoji, post, user, like_div)
        })
    }
});

function add_listiner(emoji, post, user, like_div){
    if (post.likers.includes(user.id)) {
        emoji.addEventListener("click", () => {
            like_div.innerHTML = `<i id=\"a${post.id}\" class=\"bi-hand-thumbs-up\" style=\"font-size: 1.8rem;\"></i> ${post.likes - 1}`;
            fetch("/like", {
                'method': 'POST',
                'body': JSON.stringify({
                        'post_id': post.id,
                        'like': false
                    }
                )
            })

        })
    } else {
        emoji.addEventListener("click", () => {
            like_div.innerHTML = `<i id=\"a${post.id}\" class=\"bi-hand-thumbs-up-fill\" style=\"font-size: 1.8rem;\"></i> ${post.likes + 1}`;
            fetch("/like", {
                'method': 'POST',
                'body': JSON.stringify({
                        'post_id': post.id,
                        'like': true
                    }
                )
            })
        })
    }
}