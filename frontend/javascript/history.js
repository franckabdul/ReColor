const history = JSON.parse(localStorage.getItem("ProcessedHistory")) || [];

const container = document.getElementById("history-container");

history.forEach((item) => {
  const historyItem = document.createElement("div");
  historyItem.className = "history-item";
  historyItem.innerHTML = `
                <p><strong>File:</strong> ${item.file}</p>
                <p><strong>Date:</strong> ${item.date}</p>
                <p><strong>Time:</strong> ${item.time}</p>                
            `;
  container.appendChild(historyItem);
});
