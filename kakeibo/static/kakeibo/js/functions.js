(() => {
  const deleteButtons = document.getElementsByClassName("delete-button");
  if (!deleteButtons.length) return;
  for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener("click", e => {
      const dataset = e.target.dataset;
      document.getElementById("delete-form").setAttribute("action", `/kakeibo/delete-${dataset.category}/${dataset.recordPk}/`);
    });
  }
})();

(() => {
  const deleteCategoryButtons = document.getElementsByClassName("delete-category-button");
  if (!deleteCategoryButtons.length) return;
  for (let i = 0; i < deleteCategoryButtons.length; i++) {
    deleteCategoryButtons[i].addEventListener("click", e => {
      const dataset = e.target.dataset;
      document.getElementById("delete-form").setAttribute("action", `/kakeibo/delete-category/${dataset.categoryId}/`);
    });
  }
})();