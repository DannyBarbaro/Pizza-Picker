import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-user-home',
  templateUrl: './user-home.component.html',
  styleUrls: ['./user-home.component.css']
})
export class UserHomeComponent implements OnInit {

  preferences: Object[] = [
    {name: "Meaty", select: false},
    {name: "Cheesey", select: false},
    {name: "Hawaiian", select: true},
    {name: "Supreme", select: false},
  ];
  constructor() { }

  ngOnInit() {
  }

  deletePref(name: String) {
    
  }
}
