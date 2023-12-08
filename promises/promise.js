$(document).ready(function(){
   let $div = $('#maindiv')
   
   let FAVORITE_NUMBER = 3
   axios.get(`http://numbersapi.com/${FAVORITE_NUMBER}?json`)
   .then(data => {
      console.log("first")
      console.log(data.data.text)
      return axios.get(`http://numbersapi.com/${FAVORITE_NUMBER}?json`)
   }).then(data => {
      console.log("second")
      console.log(data.data.text)
      return axios.get(`http://numberasdfasdsapi.com/${FAVORITE_NUMBER}?json`)
   }).then(data=> {
      console.log("third")
      console.log(data.data.text)
   }).catch(err => {
      console.log("this is the err")
      console.log(err)
      console.log("that was the err")
   })
   
   axios.get('')


})