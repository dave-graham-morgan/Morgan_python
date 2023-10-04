"use strict";

const $message = $("#message");
const $countdown = $("#countdown");
const $scoreDiv = $("#scoreDiv");
const $start = $("#start");
const $inputForm = $("#input-form");
const $boardContainer = $("#board-container");
const TIMER = 60;

let score = 0;

//this is the event lister on the start button
$start.on('click', start); 

//this event listeners will listen for a click on submit 
const $userResponse = $("#submit-word");
$userResponse.on('click', submitWord);
//$inputForm.show();

//this event listener will listen for an enter key so that the user can type quickly
const $attemptedText = $("#attempted-text");
$attemptedText.on('keypress', function(evt){
   if(evt.which === 13){
      evt.preventDefault();
      submitWord(evt);
   }
})

function start(evt){
   $start.hide();
   //getNewBoard();
   $inputForm.removeClass('hidden-div');
   $boardContainer.show();
   setTimer(TIMER);
}
function setTimer(timeRemaining){
   $countdown.removeClass('alert alert-danger text-danger');
   $countdown.addClass('alert alert-success text-success');
   $countdown.text(TIMER)
   const intervalId = setInterval(function () {
   //show the time remaining
   $countdown.html(timeRemaining);
   
   timeRemaining = timeRemaining-1;

   if(timeRemaining <= 10){
      $countdown.addClass('alert alert-danger text-danger');
   }
      if (timeRemaining === 0) {
         $countdown.html("TIME'S UP!");
         clearInterval(intervalId);  // Clear the interval
         cleanUp();
         
      }
   }, 1000)
};

//this function will hide the inputform and show the start button. 
function cleanUp(){
   $inputForm.addClass('hidden-div')
   $message.hide()

   //I couldn't get restart to work correctly with ajax.  I need a server refresh because of jinja so I abandoned it
   //$start.text("Play Again")
   //$start.show()
}

//this function will grab the text from the form and submit it to the server
//response is shown to the screen
async function submitWord(evt){
   evt.preventDefault();
   const userGuess = $("#attempted-text").val().toLowerCase();
   if(userGuess){
      const response = await axios({
         url: `/handle-response`,
         method: "GET",
         params: { guess: userGuess }
       })

      $message.removeClass(); //start the classes fresh

      if(response.data == "not-word"){
         $message.text(`${userGuess} is not a word`)
         $message.addClass("col-3 mx-auto justify-content-center alert alert-danger text-danger")
      }else if(response.data == "not-on-board"){
         $message.text(`${userGuess} is not on the board`)
         $message.addClass("col-3 mx-auto justify-content-center alert alert-danger text-danger")
      }else if(response.data == "previous"){
         $message.text(`you already guessed ${userGuess}`)
         $message.addClass("col-3 mx-auto justify-content-center alert alert-danger text-danger")
      }else{
         let pointValue = userGuess.length
         $message.text(`SUCCESS! ${userGuess} gives you ${pointValue}`)
         $message.addClass("col-3 mx-auto justify-content-center alert alert-success text-success")
         score = score + pointValue;
         console.debug(score);
      }

      if (score != 0){
         $scoreDiv.text(`Score: ${score}`)
      }

      //clear the form for the user
      $attemptedText.val('')
   }else{
      console.debug('nothing entered!');
   }

}  