function showPassIcon() {
    const stuPass = document.querySelector(".stu-pass");
    const icon = document.getElementById("icon");
    stuPass.addEventListener("focus", function () {
      icon.className = "fa-solid fa-lock-open";
    });
    stuPass.addEventListener("blur", function () {
      icon.className = "fa-solid fa-lock";
    });
  }
  showPassIcon();
  function showEmailIcon() {
    const stuEmail = document.querySelector(".stu-email");
    const iconEmail = document.getElementById("email");
    stuEmail.addEventListener("focus", function () {
      iconEmail.className = "fa-solid fa-envelope";
    });
    stuEmail.addEventListener("blur", function () {
      iconEmail.className = "fa-regular fa-envelope";
    });
  }
  showEmailIcon();
  function showStuLogin() {
    window.location.href = "/login";
  }
  function showEmpLogin() {
    window.location.href = "/emp_login";
  }
  