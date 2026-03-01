const container = document.getElementById("notesContainer")
const titleInput = document.getElementById("title")
const contentInput = document.getElementById("content")
const saveBtn = document.getElementById("saveBtn")


// ================= LOAD NOTES =================
async function loadNotes(){

    try{

        const res = await fetch("/api/notes")

        if(!res.ok){
            throw new Error("Failed to fetch notes")
        }

        const notes = await res.json()

        container.innerHTML = ""

        notes.forEach(n => {

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
    catch(err){
        console.error("Load error:", err)
    }
}



// ================= DELETE NOTE =================
async function deleteNote(id){

    const confirmDelete = confirm("Are you sure you want to delete this note?")

    if(!confirmDelete) return

    try{

        const res = await fetch(`/api/notes/${id}`, {
            method: "DELETE"
        })

        if(!res.ok){
            throw new Error("Delete failed")
        }

        loadNotes()

    }
    catch(err){
        console.error("Delete error:", err)
    }

}



// ================= SAVE NOTE =================
saveBtn.addEventListener("click", async () => {

    try{

        const title = titleInput.value.trim()
        const content = contentInput.value.trim()

        if(!title && !content){
            alert("Note cannot be empty")
            return
        }

        const res = await fetch("/api/notes", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title: title,
                content: content
            })

        })

        if(!res.ok){
            throw new Error("Save failed")
        }

        titleInput.value = ""
        contentInput.value = ""

        loadNotes()

    }
    catch(err){
        console.error("Save error:", err)
        alert("Failed to save note")
    }

})



// ================= INITIAL LOAD =================
document.addEventListener("DOMContentLoaded", loadNotes)