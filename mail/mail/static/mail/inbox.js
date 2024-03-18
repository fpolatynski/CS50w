document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    // Add onsubmit function
    document.querySelector('#compose-form').onsubmit = () => {
        const recipients = document.querySelector("#compose-recipients").value;
        const subject = document.querySelector("#compose-subject").value;
        const body = document.querySelector("#compose-body").value;

        fetch("emails", {
            method: 'POST',
            body: JSON.stringify(({
                recipients: recipients,
                subject: subject,
                body: body
            }))
        })
            .then(response => response.json())
            .then(result => {
            console.log(result);
            });

        load_mailbox('sent')
        return false;
    }
}

function show_mail(data){
    // Display mail
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    document.querySelector("#sender").innerHTML = `<b>From:</b> ${data.sender}`;
    document.querySelector("#recipients").innerHTML = `<b>To:</b> ${data.recipients}`;
    document.querySelector("#subject").innerHTML = `<b>Subjcet:</b> ${data.subject}`;
    document.querySelector("#timestamp").innerHTML = `<b>Timestamp:</b> ${data.timestamp}`;
    document.querySelector("#body").innerHTML = data.body;

    let archive = document.querySelector("#archive")
    // Check for archive
    if (data.archived){
        archive.innerHTML = "Unarchived"
    } else {
        archive.innerHTML = "Archived"
    }



    // Put mail as read
    fetch(`emails/${data.id}`, {
        method:'PUT',
        body: JSON.stringify({
            read: true
        })
    })

    // Add to archive
    archive.onclick = () => {
        let archive_val;
        if (archive.innerHTML === 'Archived') {
            archive_val = true;
            archive.innerHTML = 'Unarchived';
        } else {
            archive_val = false;
            archive.innerHTML = 'Archived';
        }
        // Put mail to archive
        fetch(`emails/${data.id}`, {
            method:'PUT',
            body: JSON.stringify({
                archived: archive_val
            })
        })
        // Load mail and delete
        load_mailbox('inbox');

    }

    // Reply
    const reply = document.querySelector('#reply')
    reply.onclick = () => {
        compose_email();
        document.querySelector('#compose-recipients').value = data.sender;
        document.querySelector('#compose-subject').value = `Re: ${data.subject}`;
        document.querySelector('#compose-body').value = `On ${data.timestamp} ${data.sender} wrote: ${data.body}`;

    }


}

function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    // Ask server for mails
    fetch(`/emails/${mailbox}`)
        .then( response => response.json())
        .then(data => {
            data.forEach(mail=>{
                console.log(data)
                const div = document.createElement('div');
                div.innerHTML = `<b> ${mail['sender']} </b> ${mail.subject} <div class="time">${mail.timestamp}</div>`;
                if (mail.read){
                    div.className = "mail-read"
                } else{
                    div.className = "mail";
                }
                div.addEventListener('click', () => {
                    fetch(`/emails/${mail.id}`)
                        .then(response => response.json())
                        .then(data => { show_mail(data); })
                });
                document.querySelector('#emails-view').append(div);
            })
        });
}