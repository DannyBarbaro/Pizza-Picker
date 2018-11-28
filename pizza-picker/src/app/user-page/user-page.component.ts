import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.css']
})
export class UserPageComponent implements OnInit {

  username: String = "DannyB";
  viewState: String = "userhome";

  constructor(private router: Router) { }

  ngOnInit() {
  }

  signOut() {
    this.router.navigateByUrl('/home');
  }

  changeView(view: String) {
    if(view !== this.viewState){
      this.viewState = view;
    }
  }

}
