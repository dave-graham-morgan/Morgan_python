function snakeToCamel(str) {
   answer = [];
   for (let i = 0; i<str.length;i++){
      if(str[i] === '_'){
         answer[i] = str[i+1].toUpperCase();
         i++;
      }else{
         answer[i] = str[i];
      }
   }
   return answer.join('');
}

