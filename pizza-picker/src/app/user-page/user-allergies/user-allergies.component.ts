import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-user-allergies',
  templateUrl: './user-allergies.component.html',
  styleUrls: ['./user-allergies.component.css']
})
export class UserAllergiesComponent implements OnInit {

  toppings: String[] = [];
  allergies: String[] = [];

  constructor(private router: Router, private http: HttpClient) { }

  ngOnInit() {
    this.fetchToppings();
    this.fetchAllergies()
  }

  fetchToppings() {
    this.http.get<String[]>('http://localhost:8080/toppings')
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

  allergicTo(top: String) : boolean {
    return (this.allergies.findIndex((allergy: String) => allergy === top)) !== -1;
  }

  allergyChange(top: String, state: boolean) {
    if ((state && !this.allergicTo(top)) || (!state && this.allergicTo(top))) {
      this.http.post('http://localhost:8080/allergy/' + this.router.url.split('/')[2] + '/' + top, "")
      .subscribe(x => {
        this.fetchAllergies();
      });
    }
  }
}
