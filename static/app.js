const container = document.getElementById("notesContainer")
const titleInput = document.getElementById("title")
const contentInput = document.getElementById("content")
const saveBtn = document.getElementById("saveBtn")


// LOAD NOTES
async function loadNotes(){

    const res = await fetch("/api/notes")
    const notes = await res.json()

    container.innerHTML=""

    notes.forEach(n=>{

        container.innerHTML += `
        <div class="note-card">

            <div class="note-title">${n.title || "No title"}</div>

            <div class="note-content">${n.content || ""}</div>

            <div class="note-actions">
                <button class="btn-delete" onclick="deleteNote('${n._id}')">
                    Delete
                </button>
            </div>

        </div>
        `
    })
}



// DELETE NOTE
async function deleteNote(id){

    const confirmDelete = confirm("Are you sure you want to delete this note?")

    if(!confirmDelete) return

    await fetch("/api/notes/"+id,{
        method:"DELETE"
    })

    loadNotes()
}



// SAVE NOTE
saveBtn.onclick = async ()=>{

    if(!titleInput.value && !contentInput.value){
        alert("Note cannot be empty")
        return
    }

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

    titleInput.value=""
    contentInput.value=""

    loadNotes()
}


// INITIAL LOAD
loadNotes()