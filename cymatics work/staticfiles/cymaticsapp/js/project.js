
document.addEventListener("DOMContentLoaded", function() {
// Get the modals
var editModal = document.getElementById("editModal");
var addModal = document.getElementById("addModal");

// Get the <span> element that closes the modals
var editClose = document.querySelector("#editModal .close");
var addClose = document.querySelector("#addModal .close");

// Get the cancel buttons
var editCancelBtn = document.getElementById("cancelBtn");
var addCancelBtn = document.getElementById("addCancelBtn");

// Get the add button
var addBtn = document.querySelector(".add-btn");

// Attach click event to edit buttons
var editBtns = document.getElementsByClassName("edit-btn");
for (let btn of editBtns) {
    btn.onclick = function() {
        editModal.style.display = "block";
    }
}

// Attach click event to add button
addBtn.onclick = function() {
    addModal.style.display = "block";
}

// When the user clicks on <span> (x) or cancel button, close the modals
editClose.onclick = function() {
    editModal.style.display = "none";
}

addClose.onclick = function() {
    addModal.style.display = "none";
}

editCancelBtn.onclick = function() {
    editModal.style.display = "none";
}

addCancelBtn.onclick = function() {
    addModal.style.display = "none";
}

// When the user clicks anywhere outside of the modals, close them
window.onclick = function(event) {
    if (event.target == editModal) {
        editModal.style.display = "none";
    }
    if (event.target == addModal) {
        addModal.style.display = "none";
    }
}

// Delete project card
var deleteBtns = document.getElementsByClassName("delete-btn");
for (let btn of deleteBtns) {
    btn.onclick = function() {
        var card = btn.closest(".project-card");
        card.remove();
    }
}

// Handle edit form submission
var editForm = document.getElementById("editForm");
editForm.onsubmit = function(event) {
    event.preventDefault();
    editModal.style.display = "none";
}

// Handle add form submission
var addForm = document.getElementById("addForm");
addForm.onsubmit = function(event) {
    event.preventDefault();

    // Get form values
    var type = document.getElementById("addProjectType").value;
    var status = document.getElementById("addProjectStatus").value;
    var name = document.getElementById("addProjectName").value;
    var company = document.getElementById("addCustomerCompany").value;
    var shootStart = document.getElementById("addShootStart").value;
    var shootEnd = document.getElementById("addShootEnd").value;
    var amount = document.getElementById("addProjectAmount").value;
    var location = document.getElementById("addProjectLocation").value;
    var outsourcing = document.getElementById("addOutsourcing").value;
    var reference = document.getElementById("addReference").value;

    // Create a new project card
    var newCard = document.createElement("div");
    newCard.classList.add("project-card");
    newCard.innerHTML = `
        <img src="map1.png" alt="Map" class="map">
        <div class="card-header">
            <p><b>${name}</b></p>
            <div class="dropdown">
                <button class="dropbtn">⋮</button>
                <div class="dropdown-content">
                    <a href="#" class="edit-btn">Edit</a>
                    <a href="#" class="delete-btn">Delete</a>
                </div>
            </div>
        </div>
        <p>${type}</p>
        <p>${company}</p>
        <button class="files-btn">Files</button>
        <button class="share-btn">Share</button>
    `;

    // Add the new card to the content section
    document.querySelector(".content").appendChild(newCard);

    // Re-attach event listeners to the new buttons
    var newEditBtns = newCard.getElementsByClassName("edit-btn");
    for (let btn of newEditBtns) {
        btn.onclick = function() {
            editModal.style.display = "block";
        }
    }

    var newDeleteBtns = newCard.getElementsByClassName("delete-btn");
    for (let btn of newDeleteBtns) {
        btn.onclick = function() {
            var card = btn.closest(".project-card");
            card.remove();
        }
    }

    // Clear the form and close the modal
    addForm.reset();
    addModal.style.display = "none";
}
});
   

// script for filter mechanism 
   
function setFilter(name, value) {
            document.getElementById(name).value = value;
        }

// js clear filters
function clearFilters(){
            document.getElementById('customer_company').value ='';
            document.getElementById('status').value ='';
            document.getElementById('type').value ='';
            document.forms[0].submit();
        }
   





    
 
