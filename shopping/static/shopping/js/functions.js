(() => {
  const deleteButtons = document.getElementsByClassName("delete-todo-button");
  if (!deleteButtons.length) return;
  for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener("click", e => {
      const dataset = e.target.dataset;
      document.getElementById("delete-form").setAttribute("action", `/shopping/delete-todo/${dataset.todoPk}/`)
    });
  }
})();
