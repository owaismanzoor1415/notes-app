const container = document.getElementById("notesContainer")

const titleInput = document.getElementById("title")

const contentInput = document.getElementById("content")

const saveBtn = document.getElementById("saveBtn")


async function loadNotes(){

const res = await fetch("/api/notes")

const notes = await res.json()

container.innerHTML=""

notes.forEach(n=>{

container.innerHTML += `
<div class="note-card">

<h3>${n.title}</h3>

<p>${n.content}</p>

<button onclick="deleteNote('${n._id}')">Delete</button>

</div>
`

})

}


async function deleteNote(id){

await fetch("/api/notes/"+id,{
method:"DELETE"
})

loadNotes()

}


saveBtn.onclick = async ()=>{

await fetch("/api/notes",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

title:titleInput.value,

content:contentInput.value

})

})

loadNotes()

}


loadNotes()