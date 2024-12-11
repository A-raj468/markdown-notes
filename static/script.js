// Select elements
const editor = document.getElementById("editor");
const preview = document.getElementById("preview");

// Convert the Markdown content to HTML and update preview
editor.addEventListener("input", function () {
  const markdownText = editor.value;
  const htmlContent = marked.parse(markdownText);
  preview.innerHTML = htmlContent;

  // Scroll preview to match the editor typing position
  preview.scrollTop = editor.scrollTop;
});

// Save note logic
document.getElementById("save-button").addEventListener("click", function () {
  const content = editor.value;
  const filename = document.getElementById("filename").value;
  const noteType = document.getElementById("note-type").value;

  fetch("/save", {
    method: "POST",
    body: new URLSearchParams({
      content,
      filename,
      note_type: noteType,
    }),
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  })
    .then((response) =>
      response.ok ? alert("Note saved!") : alert("Failed to save note"),
    )
    .catch((error) => alert("Error: " + error));
});
