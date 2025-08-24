async function fetchItems() {
  let res = await fetch("/items");
  let items = await res.json();
  let list = document.getElementById("items-list");
  list.innerHTML = "";
  items.forEach(item => {
    let li = document.createElement("li");
    li.innerHTML = `
      <span>${item.name} — ${item.description}</span>
      <div class="actions">
        <button onclick="editItem(${item.id}, '${item.name}', '${item.description}')">✏️</button>
        <button onclick="deleteItem(${item.id})">🗑️</button>
      </div>`;
    list.appendChild(li);
  });
}

async function createItem() {
  let name = document.getElementById("name").value;
  let description = document.getElementById("description").value;
  if (!name) return alert("Name is required");
  await fetch("/items", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, description})
  });
  document.getElementById("name").value = "";
  document.getElementById("description").value = "";
  fetchItems();
}

async function editItem(id, oldName, oldDesc) {
  let name = prompt("Update name:", oldName);
  let description = prompt("Update description:", oldDesc);
  if (name !== null) {
    await fetch(`/items/${id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({name, description})
    });
    fetchItems();
  }
}

async function deleteItem(id) {
  if (confirm("Are you sure you want to delete this item?")) {
    await fetch(`/items/${id}`, { method: "DELETE" });
    fetchItems();
  }
}

window.onload = fetchItems;
