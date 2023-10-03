"use strict";

const $message = $("#message");
const $scoreDiv = $("#scoreDiv");
const $start = $("#start");
const $blockRow = $("#block-row")

$blockRow.addClass('background-color', 'red')

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
   $start.hide()
   //myDiv.css('color', 'red');

}

//this function will grab the text from the form and submit it to the server
//response is shown to the screen
async function submitWord(evt){
   evt.preventDefault();
   const userGuess = $("#attempted-text").val();
   if(userGuess){
      const response = await axios({
         url: `/handle-response`,
         method: "GET",
         params: { guess: userGuess }
       })

      $message.removeClass(); //start the classes fresh

      if(response.data == "not-word"){
         $message.text(`${userGuess} is not a word`)
         $message.addClass("row justify-content-center alert alert-danger text-danger")
      }else if(response.data == "not-on-board"){
         $message.text(`${userGuess} is not on the board`)
         $message.addClass("row justify-content-center alert alert-danger text-danger")
      }else if(response.data == "previous"){
         $message.text(`you already guessed ${userGuess}`)
         $message.addClass("row justify-content-center alert alert-danger text-danger")
      }else{
         let pointValue = userGuess.length
         $message.text(`SUCCESS! ${userGuess} gives you ${pointValue}`)
         $message.addClass("row justify-content-center alert alert-success text-success")
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