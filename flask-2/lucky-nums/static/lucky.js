/** processForm: get data from form and make AJAX call to our API. */

function processForm(evt) {
   if (evt){
      evt.preventDefault();
      let name = $('#name');
      let year = $('#year');
      let email = $('#email');
      let color = $('#color');

      let formData = {
         name: name.val(),
         year: year.val(),
         email: email.val(),
         color: color.val()
      };
      console.log(formData);

      $.ajax({
         url: '/api/get-lucky-num',
         method: 'POST',
         contentType: 'application/json',
         data: JSON.stringify(formData),
         success: function(data){
            handleResponse(data);
         }
      });
   }
}

/** handleResponse: deal with response from our lucky-num API. */

function handleResponse(resp) {
   const $colorErr = $("#color-err");
   $colorErr.text('');
   const $emailErr = $("#email-err");
   $emailErr.text('');
   const $nameErr = $("#name-err");
   $nameErr.text('');
   const $yearErr = $("#year-err")
   $yearErr.text('')

   if (resp.errors){
      if(resp.errors.color){
         $colorErr.text(resp.errors.color)
      }
      if(resp.errors.email){
         $emailErr.text(resp.errors.email)
      }
      if(resp.errors.name){
         $nameErr.text(resp.errors.name)
      }
      if(resp.errors.year){
         $yearErr.text(resp.errors.year)
      }
   }else{
      const results = $("#lucky-results");
      results.append(`Your lucky number is ${resp.num.num} (${resp.num.fact})`)
      results.append(`<br> Your birth year (${resp.year.year}) fact is: ${resp.year.fact}`)

   }
}


$("#lucky-form").on("submit", processForm);
