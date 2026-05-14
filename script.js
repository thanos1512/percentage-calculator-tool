function calculatePercentage() {

  let obtained =
    document.getElementById("obtained").value;

  let total =
    document.getElementById("total").value;

  if (obtained === "" || total === "") {
    document.getElementById("result").innerText =
      "Please enter all values";
    return;
  }

  let percentage = (obtained / total) * 100;

  document.getElementById("result").innerText =
    "Percentage: " + percentage.toFixed(2) + "%";
}