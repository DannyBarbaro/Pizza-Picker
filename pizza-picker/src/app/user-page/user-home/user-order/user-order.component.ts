import { Component, OnInit } from '@angular/core';
import { Order } from '../../../data-objects'
@Component({
  selector: 'app-user-order',
  templateUrl: './user-order.component.html',
  styleUrls: ['./user-order.component.css']
})
export class UserOrderComponent implements OnInit {

  order: Order;
  orderbody: String = "";
  constructor() { }

  ngOnInit() {
    let count: number = 0;
    for (let comp of this.order.components) {
      count += comp.sliceCount;
      this.orderbody += "Order " + comp.sliceCount + " slices of ";
      for(let top of comp.toppings) {
        this.orderbody += top + " ";
      }
      this.orderbody += "\n";
    }
    this.orderbody += " This is " + count/8 + " total pizzas";
  }

}
