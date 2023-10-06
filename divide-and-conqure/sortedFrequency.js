/*Given a sorted array and a number, write a function called sortedFrequency 
that counts the occurrences of the number in the array */

function findSortedFrequency (arr, num){
   //initialize the variables we will be using
   let rightIdx = arr.length -1;
   let leftIdx = 0;
   let pointer = Math.floor(rightIdx/2);

   //check that the number exists in the array by comparing with higest and lowest
   if(num > arr[rightIdx] || num < arr[leftIdx]){
      return -1;
   }
   while(true){
      if(arr[pointer] === num){
         //find index of uppermost occurance of num
         const upperMostOccurance = findUpper(arr, num, pointer, arr.length-1)
         //find index of lowermost occurance of num
         const lowerMostOccurance = findLower(arr, num, pointer, 0)
         return upperMostOccurance - lowerMostOccurance + 1 //add one so that we include each end
      }else if (arr[pointer] < num){
         leftIdx = pointer;
         pointer = Math.floor((pointer + rightIdx)/2)
      }else{ 
         rightIdx = pointer;
         pointer = Math.floor((pointer + leftIdx)/2)
      }
   }

   function findUpper(arr, num, lowerIdx, upperIdx){
   
      if(arr[upperIdx] === num){return upperIdx}

      let pointer = Math.floor((upperIdx + lowerIdx)/2);
      while(pointer !== lowerIdx && pointer !== upperIdx)
         if(arr[pointer] === num){
            lowerIdx = pointer;
            pointer = Math.floor((pointer + upperIdx)/2);
         } else if(arr[pointer] < num){
            lowerIdx = pointer;
            pointer = Math.floor((pointer + upperIdx)/2)
         }else{//arr[pointer] > num
            upperIdx = pointer
            pointer = Math.floor((pointer + lowerIdx)/2)
         }
      return pointer
   }

   function findLower(arr, num, upperIdx,lowerIdx){
      if(arr[lowerIdx] === num){return lowerIdx}

      let pointer = Math.floor((upperIdx + lowerIdx)/2);
      while(pointer !== lowerIdx && pointer !== upperIdx){
         if(arr[pointer] === num){
            upperIdx = pointer;
            pointer = Math.floor((pointer + lowerIdx)/2);
         }else if(arr[pointer] < num){
            lowerIdx = pointer;
            pointer = Math.floor((pointer + upperIdx)/2);
         }else{
            upperIdx = pointer;
            pointer = Math.floor((pointer + upperIdx)/2);
         }
      }
      return pointer;
   }
   
   console.debug(`right: ${rightIdx}, left: ${leftIdx}, point: ${pointer}`)

}




// findSortedFrequency([1,1,2,2,2,2,3],2) // 4
// findSortedFrequency([1,1,2,2,2,2,3],3) // 1
// findSortedFrequency([1,1,2,2,2,2,3],1) // 2
// findSortedFrequency([1,1,2,2,2,2,3],4) // -1
