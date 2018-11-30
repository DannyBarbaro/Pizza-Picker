import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-user-friends',
  templateUrl: './user-friends.component.html',
  styleUrls: ['./user-friends.component.css']
})
export class UserFriendsComponent implements OnInit {

  friendAddResult: String = "";
  addField: String = "";
  friends: String[] = [];

  constructor(private router: Router, private http: HttpClient) { }

  ngOnInit() {
    this.fetchFriends();
  }

  fetchFriends() {
    this.http.get<String[]>('http://localhost:8080/friends/' + this.router.url.split('/')[2])
      .subscribe((data: String[]) => {
        this.friends = data;
      });
  }

  addFriend() {
    if (this.addField.length != 0) {
      this.http.get<Boolean>('http://localhost:8080/userExists/' + this.router.url.split('/')[2])
        .subscribe((data: Boolean) => {
          if (data) {
            this.http.post('http://localhost:8080/friend/' + this.router.url.split('/')[2] + '/' + this.addField, "")
              .subscribe(x => this.fetchFriends())
          }
        });
    }
  }

  unfriend(name: String) {
    this.http.delete('http://localhost:8080/unfriend/' + this.router.url.split('/')[2] + '/' + name)
      .subscribe(x => {
        this.fetchFriends();
      });
  }

}
