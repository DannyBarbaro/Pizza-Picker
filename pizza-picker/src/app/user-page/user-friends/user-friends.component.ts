import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-user-friends',
  templateUrl: './user-friends.component.html',
  styleUrls: ['./user-friends.component.css']
})
export class UserFriendsComponent implements OnInit {

  friendAddResult: String = "";
  addField: String = "";

  constructor() { }

  ngOnInit() {
  }

  addFriend(){

  }

  unfriend(name: String) {
    
  }

}
