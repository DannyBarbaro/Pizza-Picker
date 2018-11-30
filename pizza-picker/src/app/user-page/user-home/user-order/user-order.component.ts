import { Component, OnInit } from '@angular/core';
import { Order } from '../../../data-objects'
import { BsModalRef } from 'ngx-bootstrap';
@Component({
  selector: 'app-user-order',
  templateUrl: './user-order.component.html',
  styleUrls: ['./user-order.component.css']
})
export class UserOrderComponent implements OnInit {

  order: Order;
  orderbody: String = "";
  constructor(public bsModalRef: BsModalRef) { }

  ngOnInit() {
    let count: number = 0;
    for (let comp of this.order.components) {
      count += comp.sliceCount;
      this.orderbody += "Order " + comp.sliceCount + " slices of ";
      for(let top of comp.toppings) {
        this.orderbody += top + ", ";
      }
      if (comp.toppings.length === 0) {
        this.orderbody += "plain"
      } else {
        this.orderbody = this.orderbody.slice(0, -2)
      }
      this.orderbody += ".\n";
    }
    this.orderbody += " This is " + count/8 + " total pizzas.";
  }

}
