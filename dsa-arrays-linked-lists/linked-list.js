/** Node: node for a singly linked list. */

class Node {
  constructor(val) {
    this.val = val;
    this.next = null;
  }
}

/** LinkedList: chained together nodes. */

class LinkedList {
  constructor(vals = []) {
    this.head = null;
    this.tail = null;
    this.length = 0;

    for (let val of vals) this.push(val);
  }

  /** push(val): add new value to end of list. */

  push(val) {
    let newNode = new Node(val);
    if(!this.head){
      this.head = newNode;
    }
    if(this.tail){
      this.tail.next = newNode
    }
    this.tail = newNode;
    this.length =this.length + 1;
  }

  /** unshift(val): add new value to start of list. */

  unshift(val) {
    
    let newNode = new Node(val);
    if(this.head){
      let temp = this.head;
      this.head = newNode;
      newNode.next = temp;
    }else{
      this.head = newNode;
      this.tail = newNode;
    }
    this.length = this.length + 1;
  }

  /** pop(): return & remove last item. */

  pop() {
    if(this.head){
      let currNode = this.head;
      
      if(this.length === 1){
        let tempNode = this.head;
        this.tail = null;
        this.head = null;
        this.length = 0;

        return tempNode.val;
      }else{
        for(let i = 0; i<this.length-2; i++){
          currNode = currNode.next
        }

        let nodeToDelete = currNode.next;

        currNode.next = null;

        this.tail = currNode;
        this.length = this.length - 1;

        return nodeToDelete.val;
      }
      
    }
  }

  /** shift(): return & remove first item. */

  shift() {
    if(this.head && this.head.next){
      let temp = this.head;
      this.head = this.head.next;
      this.length = this.length -1;
      return temp.val;

    }else if(this.head){
      let temp = this.head;
      this.head = null;
      this.tail = null;
      this.length = 0;
      return temp.val;
    }
  }

  /** getAt(idx): get val at idx. */

  getAt(idx) {
    let index = 0;
    let currNode = this.head;
    while (idx !== index){
      currNode = currNode.next;
      index += 1;
    }
    return currNode.val;
  }

  /** setAt(idx, val): set val at idx to val */

  setAt(idx, val) {
    let index = 0;
    let currNode = this.head;
    while(idx !== index){
      currNode = currNode.next;
      index += 1;
    }
    currNode.val = val;
  }

  /** insertAt(idx, val): add node w/val before idx. */

  insertAt(idx, val) {
    let isLast = false;
    if(this.length === idx){
      isLast = true;
    }


    let newNode = new Node(val);
    let index = 0;
    let currNode = this.head;

    if(this.length === 0){
      this.length = 1;
      this.head = newNode;
      this.tail = newNode
      return;
    }

    while(idx-1!==index){
      if(currNode.next){
        currNode = currNode.next;
      }
      index += 1;
    }

    let nextNode = currNode.next;
    currNode.next = newNode;
    newNode.next = nextNode;
    this.length += 1;
    if(isLast){
      this.tail = newNode;
    }
  }

  /** removeAt(idx): return & remove item at idx, */

  removeAt(idx) {
    //handle case where node to remove is head node
    if(idx === 0){
      if (this.head.next){
        nextNode = this.head.next;
        this.head = nextNode;
        this.length--;
      }else{ //if there is no head.next, then there is only one node in the list
        this.head = null;
        this.tail = null;
        this.length = 0;
        return;
      }
    }
    //handle the case where node to remove is tail (we've done this already)
    if (idx === this.length){  
      this.pop();
      return;
    }
    //check for error condition
    if(idx > this.length){
      return;
    }

    //all other cases
    let index = 0;
    let currNode;
    let previousNode;
    while(idx !== index){
      previousNode = currNode;
      currNode = currNode.next;
      index++;
    }
    previousNode.next = currNode;
    this.length --;

  }

  /** average(): return an average of all values in the list */

  average() {
    //handle zero size list
    if(this.length ===0){
      return 0;
    }
    let count = 0
    let sum = 0
    let currNode = this.head
    while (currNode.next){
      sum = sum + currNode.val;
      count++;
      currNode = currNode.next;
    }
    sum = sum + currNode.val;
    count++
    return sum/count;
  }
}

module.exports = LinkedList;
