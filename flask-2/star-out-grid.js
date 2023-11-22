function starOutGrid(grid) {
   let rowsToStar = new Set();
   let columnsToStar = new Set();
   
   //its clunky but lets find the rows and columnns that need *
   for(let i = 0;i<grid.length;i++)  {
      for(let j = 0;j<grid[i].length;j++){
         if(grid[i][j] === '*'){
            rowsToStar.add(i);
            columnsToStar.add(j);
         }
      }
   }

   //now lets * them!
   for(let i = 0;i<grid.length;i++)  {
      for(let j = 0;j<grid[i].length;j++){
         if(rowsToStar.has(i) || columnsToStar.has(j)){
            grid[i][j] = '*'
         }
      }
   }

   return grid
}