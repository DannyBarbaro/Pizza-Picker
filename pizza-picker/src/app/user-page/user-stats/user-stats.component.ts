import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-user-stats',
  templateUrl: './user-stats.component.html',
  styleUrls: ['./user-stats.component.css']
})
export class UserStatsComponent implements OnInit {

  orders: String = "17";
  bestfriend: String = "Niha";
  topToppings: String = "Pineapple and Ham";
  
  constructor() { }

  ngOnInit() {
  }

}
