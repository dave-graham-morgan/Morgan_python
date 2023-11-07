$(function(){

const $li = $('#ulElement');

async function getCupcakes(){
   const response = await axios.get('http://localhost:8080/api/cupcakes')
   console.log(response.data.cupcakes)

   for (cupcake of response.data.cupcakes){
      const li = `<li><a href="">${cupcake.size} ${cupcake.flavor}</a></li>`
      $('#ulElement').append(li)
   }

}

$('#cupcakeForm').on("submit", async function(evt){
   evt.preventDefault();

   let flavor = $('#flavor').val();
   let rating = $('#rating').val();
   let size = $('#size').val();
   let image = $('#image').val();
   const response = await axios.post('/api/cupcakes', {flavor, rating, size, image});
   window.location.reload();
})

getCupcakes();


});