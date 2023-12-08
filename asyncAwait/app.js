$(document).ready(function(){

   async function getPokemon(){
      let promise1 = axios.get('http://numbersapi.com/3?json')
      let promise2 = axios.get('http://numbersapi.com/3?json')
      let promise3 = axios.get('http://numbersapi.com/3?json')

      let firstFact = await promise1;
      let secondFact = await promise2;
      let thirdFact = await promise3;

      console.log(firstFact.data.text);
      console.log(secondFact.data.text);
      console.log(thirdFact.data.text);
   }
   getPokemon();


   async function getPokemonPromiseAll(){
      let allThree = await Promise.all([axios.get('http://numbersapi.com/4?json'), 
                     axios.get('http://numbersapi.com/4?json'), 
                     axios.get('http://numbersapi.com/4?json')])
      console.log(allThree[0].data.text);
      console.log(allThree[1].data.text);
      console.log(allThree[2].data.text);
   }
   getPokemonPromiseAll();

   
   
   let newDeckID = undefined;
   let cardsLeft = undefined;

   async function deckOfCards(){
      let resp = await axios.get('https://deckofcardsapi.com/api/deck/new/')
      newDeckID = resp.data.deck_id;
      cardsLeft = resp.data.remaining
      await axios.get(`https://deckofcardsapi.com/api/deck/${newDeckID}/shuffle/`)
   }

   async function getNewCard(){
      let resp = await axios.get(`https://deckofcardsapi.com/api/deck/${newDeckID}/draw/?count=1`)
      cardsLeft = resp.data.remaining
      suit = resp.data.cards[0].suit
      value = resp.data.cards[0].value

      let $cardDiv = $('#drawn-card')
      $cardDiv.append(`${value} of ${suit}`)
      $cardDiv.append('<br>')

      let $cardsLeft = $('#cards-left')
      $cardsLeft.text(`there are ${cardsLeft} cards left`)

   }

   deckOfCards();


   $('#new-card').on('click', getNewCard)
})