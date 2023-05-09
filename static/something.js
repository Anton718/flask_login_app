'use strict';

window.onload = function retrieve_storage() {
    JSON.parse(localStorage.getItem("posts")).forEach((elem)=>createOldPosts(elem));
} 
function createOldPosts(elem){
    const p = document.createElement('p');
    if (elem.includes("Welcome")) {
        p.innerText = "";
    } else {
    p.innerText = elem;
    p.style.color = "grey";
    inner.append(p);
    }
}
const greeting = document.querySelector('.greeting');
const chatname = document.querySelector('#chatname');
chatname.addEventListener("input", ()=> greeting.textContent = `Welcome, ${chatname.value}!`);
const inner = document.querySelector('.inner')
const text = document.querySelector('#text')
const submit = document.querySelector('.submit')
submit.value = 'Post';
const clear = document.querySelector('.clear')
clear.value = 'Clear Chat';
submit.addEventListener('click', async ()=> {
    const post_div = document.createElement('div');
    const p_date = document.createElement('p');
    p_date.textContent = new Date().toLocaleString();
    p_date.style.fontSize = '10px';
    const post = document.createElement('p');
    post.textContent = `${chatname.value} posted: ${text.value}`;
    post.style.color = "green";
    post_div.append(p_date);
    post_div.append(post);
    inner.append(post_div);
    text.value = "";
    get_storage()
});

    clear.addEventListener('click', ()=> {
        localStorage.clear();
        inner.innerHTML = "";
    })

    function get_storage() {
        let arr =[];
        let posts = document.querySelectorAll('p');
        posts.forEach((elem)=>{arr.push(elem.textContent)});
        localStorage.setItem("posts", JSON.stringify(arr));
    }
   