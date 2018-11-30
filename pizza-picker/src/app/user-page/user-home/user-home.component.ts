import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { PreferenceSet, Preference, Order } from '../../data-objects';

@Component({
  selector: 'app-user-home',
  templateUrl: './user-home.component.html',
  styleUrls: ['./user-home.component.css']
})
export class UserHomeComponent implements OnInit {

  preferences: PreferenceSet[] = [];
  errorLabel: String = "";
  radioModel = 'Middle';
  modalPreferences: Preference[] = [];
  toppings: String[] = [];

  constructor(private router: Router, private http: HttpClient) { }

  ngOnInit() {
    this.errorLabel = ""
    this.fetchPrefSets();
  }

  fetchPrefSets() {
    this.http.get<PreferenceSet[]>('http://localhost:8080/prefsets/' + this.router.url.split('/')[2])
      .subscribe((data: PreferenceSet[]) => this.preferences = data);
  }

  //maybe
  currentPrefChange() {

  }

  deletePref(pref: PreferenceSet) {
    if (pref.isCurrent) {
      this.errorLabel = "You cannot delete your current preference set"
    } else {
      this.http.delete('http://localhost:8080/removePref/' + this.router.url.split('/')[2] + '/' + pref.id)
        .subscribe(x => this.fetchPrefSets());
    }
  }

  editPref(prefs: Preference[]) {
    this.modalPreferences = prefs
  }

  savePref() {

  }

  friends: String[] = [];
  myOrder: String[] = [];
  pullFriends() {
    this.http.get<String[]>('http://localhost:8080/friends/' + this.router.url.split('/')[2])
      .subscribe((data: String[]) => {
        this.friends = data;
      });
  }
  addToOrder(friend: String) {
    if (this.myOrder.findIndex((orderMember: String) => orderMember === friend) === -1) {
      this.myOrder.push(friend);
    }
  }

  removeFromOrder(person: String) {
    this.myOrder = this.myOrder.filter((orderMember: String) => orderMember !== person);
  }

  placeOrder() {
    this.http.post('http://localhost:8080/order', this.myOrder)
    .subscribe((order: Order) => {
      //TODO
      console.log(order.pizza);
    });
  }
}
