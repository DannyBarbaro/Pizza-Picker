import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-user-stats',
  templateUrl: './user-stats.component.html',
  styleUrls: ['./user-stats.component.css']
})
export class UserStatsComponent implements OnInit {

  orders: number = 0;
  bestfriend: String = "";
  topTopping: String = "";

  constructor(private router: Router, private http: HttpClient) { }

  ngOnInit() {
    this.getTotalOrders();
    this.getBestFriend();
    this.getTopTopping();
  }

  getTotalOrders() {
    this.http.get<number>('http://localhost:8080/stat/total/' + this.router.url.split('/')[2])
      .subscribe((data: number) => this.orders = data);
  }

  getBestFriend() {
    this.http.get<String>('http://localhost:8080/stat/bestfriend/' + this.router.url.split('/')[2])
      .subscribe((data: String) => this.bestfriend = data);
  }

  getTopTopping() {
    this.http.get<String>('http://localhost:8080/stat/favTop/' + this.router.url.split('/')[2])
      .subscribe((data: String) => this.topTopping = data);
  }

}
