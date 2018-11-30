import { Component, OnInit } from '@angular/core';
import { Order } from '../../../data-objects'
@Component({
  selector: 'app-user-order',
  templateUrl: './user-order.component.html',
  styleUrls: ['./user-order.component.css']
})
export class UserOrderComponent implements OnInit {

  order: Order;
  
  constructor() { }

  ngOnInit() {
  }

}
