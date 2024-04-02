// When DOM content is loaded
document.addEventListener('DOMContentLoaded', () => {
    const user_id = document.getElementById('user_id');
    let id = 1;
    if (user_id) {
        id = JSON.parse(user_id.textContent);
    } else {
        // Add onsubmit function
        document.querySelector('#asd').onclick = () => {
            const text = document.querySelector("#new_post-text").value;
            fetch("/new_post", {
                method: 'POST',
                body: JSON.stringify({
                    text: text
                })
            })
            document.querySelector("#new_post-text").value = "";
        }
    }

    let page = 1;
    newMails();

    document.querySelector("#next").onclick = () => {
        page += 1;
        newMails();
    }

    document.querySelector("#previous").onclick = () => {
        if (page > 1) {
            page -= 1;
            newMails();
        }
    }

    function newMails() {
        let to_fetch = "";
        if (user_id) {
            to_fetch = `posts?page=${page}&owner=${id}`
        } else {
            to_fetch = `posts?page=${page}`
        }
        fetch(to_fetch)
            .then(response => response.json())
            .then(data => {
                display(data);
                console.log(data)
            });
        window.scrollTo(0, 0);
    }

    function display(data) {
        document.querySelector("#all_posts").innerHTML = "";
        const user = data["user"]
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
            owner_div.innerHTML = `<a href=\"${post.owner.id}\">${post.owner.username}</a> ${post.id}`;
            if (post.likers.includes(user.id)) {
                like_div.innerHTML = `<i id=\"a${post.id}\" class=\"bi-hand-thumbs-up-fill\" style=\"font-size: 1.8rem;\"></i> ${post.likes}`;
            } else {
                like_div.innerHTML = `<i id=\"a${post.id}\" class=\"bi-hand-thumbs-up\" style=\"font-size: 1.8rem;\"></i> ${post.likes}`;
            }
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
})

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

