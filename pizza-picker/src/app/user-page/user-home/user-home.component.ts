import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { PreferenceSet, Preference, Order } from '../../data-objects';
import { BsModalRef } from 'ngx-bootstrap/modal';

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

  constructor(private router: Router, private http: HttpClient) { }

  ngOnInit() {
    this.errorLabel = ""
    this.fetchPrefSets();
  }

  fetchPrefSets() {
    this.http.get<PreferenceSet[]>('http://localhost:8080/prefsets/' + this.router.url.split('/')[2])
      .subscribe((data: PreferenceSet[]) => this.preferences = data);
  }

  deletePref(pref: PreferenceSet) {
    if (pref.isCurrent) {
      this.errorLabel = "You cannot delete your current preference set"
    } else {
      this.http.delete('http://localhost:8080/removePref/' + this.router.url.split('/')[2] + '/' + pref.id)
        .subscribe(x => this.fetchPrefSets());
    }
  }

  toppings: String[] = [];
  allergies: String[] = [];
  prefSetName: String = "";
  prefDisplay: Preference[] = [];
  fetchToppings() {
    this.http.get<String[]>('http://localhost:8080/toppings/')
      .subscribe((data: String[]) => {
        this.toppings = data;
      });
  }

  fetchAllergies() {
    this.http.get<String[]>('http://localhost:8080/allergies/' + this.router.url.split('/')[2])
      .subscribe((data: String[]) => {
        this.allergies = data;
      });
  }

  allergicTo(top: String): boolean {
    return (this.allergies.findIndex((allergy: String) => allergy === top)) !== -1;
  }

  openPref(currentPref?: Preference[]) {
    this.fetchToppings();
    this.fetchAllergies();
    let neededTops: String[] = this.toppings.filter((top: String) => !this.allergicTo(top));
    this.prefDisplay = [];
    if (currentPref) {
      for (let top of neededTops) {
        let index: number = currentPref.findIndex((pref: Preference) => pref.topping === top);
        if (index !== -1) {
          this.prefDisplay.push({ topping: <string>top, score: currentPref[index].score });
        } else {
          this.prefDisplay.push({ topping: <string>top, score: 0 });
        }
      }
    } else {
      for (let top of neededTops) {
        this.prefDisplay.push({ topping: <string>top, score: 0 });
      }
    }
  }

  savePref(modal: BsModalRef) {
    if (this.prefSetName.length != 0) {
      //TODO push the data to the db
      modal.hide();
    }
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
