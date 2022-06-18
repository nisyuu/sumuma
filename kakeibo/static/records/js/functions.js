(() => {
  const deleteButtons = document.getElementsByClassName("delete-button");
  if (!deleteButtons.length) return;
  for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener("click", e => {
      const dataset = e.target.dataset;
      document.getElementById("delete-form").setAttribute("action", `/kakeibo/records/delete-${dataset.category}/${dataset.recordPk}/`)
    });
  }
})();

(() => {
  const deleteButtons = document.getElementsByClassName("delete-latest-button");
  if (!deleteButtons.length) return;
  for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener("click", e => {
      const dataset = e.target.dataset;
      document.getElementById("delete-form").setAttribute("action", `/kakeibo/records/delete-latest-${dataset.category}/${dataset.recordPk}/`)
    });
  }
})();
