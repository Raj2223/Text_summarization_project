document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("button");

  // Show the button when the page is loaded
  button.style.display = "block";

  button.addEventListener("click", function () {
      button.classList.add("redirect-animation");

      setTimeout(function () {
          window.location.href = servicesUrl;
      }, 300);
  });
  window.addEventListener("pageshow", function(event) {
    // Check if the event is fired due to navigating back
    if (event.persisted) {
        // Reload the page
        window.location.reload();
    }
});
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
      e.preventDefault();

      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
          window.scrollTo({
              top: target.offsetTop,
              behavior: 'smooth'
          });
      }
  });
});

function toggleMobileNav() {
  console.log("Function toggleMobileNav called");
  $(".mobile-nav-toggle").on("click", function (e) {
      console.log("Toggle button clicked");
      $("#navbar").toggleClass("navbar-mobile");
      $(this).toggleClass("bi-list bi-x");
  });
}
toggleMobileNav();


// file upload div
function handleFileSelect() {
  var fileInput = document.getElementById("file-upload");
  var fileNameDisplay = document.getElementById("file-name");
  var textDiv = document.querySelector(".text-div");
  var or = document.querySelector(".or");
  var textConntainer = document.querySelector(".text-container");
  var customFileUploader = document.querySelector(".custom-file-upload");
  var uploadContainer = document.querySelector(".upload-container");
  var rmbutton = document.getElementById("removebutton");
  var smbutton = document.getElementById("submitButton");
  if (fileInput.files && fileInput.files[0]) {
    fileNameDisplay.textContent = fileInput.files[0].name;
    customFileUploader.style.display = "none";
    textConntainer.style.display = "none";
    or.style.display = "none";
    rmbutton.style.display = "block";
    uploadContainer.style.width = "100%";
    smbutton.style.display = "block";
    window.addEventListener("resize", function () {
      if (window.matchMedia("(max-width: 840px)").matches) {
        textDiv.style.top = "0px";
      } else {
        textDiv.style.top = "130px";
      }
    });
  } else {
    fileNameDisplay.textContent = "No file chosen";
    rmbutton.style.display = "none";
    smbutton.style.display = "none";
  }
}

function removeFile() {
  var fileInput = document.getElementById("file-upload");
  var customFileUploader = document.querySelector(".custom-file-upload");
  var fileNameDisplay = document.getElementById("file-name");
  var textConntainer = document.querySelector(".text-container");
  var or = document.querySelector(".or");
  var rmbutton = document.getElementById("removebutton");
  var smbutton = document.getElementById("submitButton");
  // Clear the file input if there is any name written
  fileInput.value = null;

  // Reset the file name display
  fileNameDisplay.textContent = "No file chosen";
  customFileUploader.style.display = "block";
  textConntainer.style.display = "block";
  or.style.display = "block";
  rmbutton.style.display = "none";
  smbutton.style.display = "none";
}
function handleTextInput() {
  var text = document.getElementById("text1").value;
  var customFileUploader = document.querySelector(".custom-file-upload");
  var or = document.querySelector(".or");
  var fileNameDisplay = document.getElementById("file-name");
  var smbutton = document.getElementById("submitButton");
  if (text.trim() !== "") {
    customFileUploader.style.display = "none";
    or.style.display = "none";
    fileNameDisplay.style.display = "none";
    smbutton.style.display = "block";
  } else {
    customFileUploader.style.display = "block";
    or.style.display = "block";
    fileNameDisplay.style.display = "block";
    smbutton.style.display = "none";
  }
}
function validateCheckbox() {
  var checkboxes = document.querySelectorAll('input[name="models"]:checked');
  var messageDiv = document.getElementById('messageDiv');

  if (checkboxes.length < 2 ) {
    messageDiv.textContent = 'Please choose at least two models.';
    return false;
  }
  else if ( checkboxes.length > 4){
    messageDiv.textContent = 'Please choose at most four models.';
    return false;
  } 
  else {
    messageDiv.textContent = '';
    return true;   
  }
}

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("myForm").addEventListener("submit", function (e) {
    // e.preventDefault()
      var isValid = validateCheckbox();
      console.log("Form submitted");
    
      if (isValid) {
          console.log("Validation passed");
          // document.getElementById('myForm').submit();
      } else {
          console.log("Validation failed");
          e.preventDefault();
      }
  });
});



var checkboxes = document.querySelectorAll('input[name="models"]');
checkboxes.forEach(function(checkbox) {
  checkbox.addEventListener('change', validateCheckbox);
});


//--------------------------------- snake game js code-------------------------------


const playBoard = document.querySelector(".play-board");
const scoreElement = document.querySelector(".score");
const highScoreElement = document.querySelector(".high-score");
const controls = document.querySelectorAll(".controls i");

let gameOver = false;
let foodX, foodY;
let snakeX = 5,
  snakeY = 5;
let velocityX = 0,
  velocityY = 0;
let snakeBody = [];
let setIntervalId;
let score = 0;

// Getting high score from the local storage
let highScore = localStorage.getItem("high-score") || 0;
highScoreElement.innerText = `High Score: ${highScore}`;

const updateFoodPosition = () => {
  // Passing a random 1 - 30 value as food position
  foodX = Math.floor(Math.random() * 30) + 1;
  foodY = Math.floor(Math.random() * 30) + 1;
};

const handleGameOver = () => {
  // Resetting game state
  gameOver = false;
  snakeX = 5;
  snakeY = 5;
  velocityX = 0;
  velocityY = 0;
  snakeBody = [];
  score = 0;
  updateFoodPosition();
  scoreElement.innerText = `Score: ${score}`;
  clearInterval(setIntervalId);
  setIntervalId = setInterval(initGame, 100);
  alert("Game Over! Press OK to replay...");
};


const changeDirection = (e) => {
  // Changing velocity value based on key press
  if (e.key === "ArrowUp" && velocityY != 1) {
    velocityX = 0;
    velocityY = -1;
  } else if (e.key === "ArrowDown" && velocityY != -1) {
    velocityX = 0;
    velocityY = 1;
  } else if (e.key === "ArrowLeft" && velocityX != 1) {
    velocityX = -1;
    velocityY = 0;
  } else if (e.key === "ArrowRight" && velocityX != -1) {
    velocityX = 1;
    velocityY = 0;
  }
};

// Calling changeDirection on each key click and passing key dataset value as an object
controls.forEach((button) =>
  button.addEventListener("click", () =>
    changeDirection({ key: button.dataset.key })
  )
);

const initGame = () => {
  if (gameOver) return handleGameOver();
  let html = `<div class="food" style="grid-area: ${foodY} / ${foodX}"></div>`;

  // Checking if the snake hit the food
  if (snakeX === foodX && snakeY === foodY) {
    updateFoodPosition();
    snakeBody.push([foodY, foodX]); // Pushing food position to snake body array
    score++; // increment score by 1
    highScore = score >= highScore ? score : highScore;
    localStorage.setItem("high-score", highScore);
    scoreElement.innerText = `Score: ${score}`;
    highScoreElement.innerText = `High Score: ${highScore}`;
  }
  // Updating the snake's head position based on the current velocity
  snakeX += velocityX;
  snakeY += velocityY;

  // Shifting forward the values of the elements in the snake body by one
  for (let i = snakeBody.length - 1; i > 0; i--) {
    snakeBody[i] = snakeBody[i - 1];
  }
  snakeBody[0] = [snakeX, snakeY]; // Setting first element of snake body to current snake position

  // Checking if the snake's head is out of wall, if so setting gameOver to true
  if (snakeX <= 0 || snakeX > 30 || snakeY <= 0 || snakeY > 30) {
    return (gameOver = true);
  }

  for (let i = 0; i < snakeBody.length; i++) {
    // Adding a div for each part of the snake's body
    html += `<div class="head" style="grid-area: ${snakeBody[i][1]} / ${snakeBody[i][0]}"></div>`;
    // Checking if the snake head hit the body, if so set gameOver to true
    if (
      i !== 0 &&
      snakeBody[0][1] === snakeBody[i][1] &&
      snakeBody[0][0] === snakeBody[i][0]
    ) {
      gameOver = true;
    }
  }
  playBoard.innerHTML = html;
};

updateFoodPosition();
setIntervalId = setInterval(initGame, 100);
document.addEventListener("keyup", changeDirection);

// Function to show preloader
function showPreloader() {
  document.querySelector('.loading-screen').style.display = "block";
  document.getElementById('body').style.overflow = 'hidden';
}

// Function to hide preloader
function hidePreloader() {
  document.querySelector('.loading-screen').style.display = "none";
  document.getElementById('body').style.overflow='auto'
}

// Submit form handler
document.getElementById("myForm").addEventListener("submit", function() {
  // Show preloader when form is submitted
  showPreloader();
});

// Hide preloader when page is fully loaded
window.addEventListener("load", function() {
  // Hide preloader when page is loaded
  hidePreloader();
});