import { Component, OnInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-signup',
  templateUrl: './login-signup.component.html',
  styleUrls: ['./login-signup.component.css']
})
export class LoginSignupComponent implements OnInit {

  viewSwitcher: boolean;
  entryError: String = "";
  signUpError: String = "";
  constructor(public bsModalRef: BsModalRef, private router: Router) { }

  ngOnInit() {
  }

  signIn() {
    //http call for log in
    let loginSuccessful: boolean = true;
    if (loginSuccessful) {
      //route to the next page
      this.bsModalRef.hide();
      this.router.navigateByUrl('/userpage');
    } else {
      this.entryError = "Incorrect Username or Password";
    }
  }

  signUp() {
    //http call to check if username is available
    let usernameAvailable: boolean = true;
    let passwordMatch: boolean = true;
    if (usernameAvailable) {
      if (passwordMatch) {
        this.bsModalRef.hide();
        this.router.navigateByUrl('/userpage');
      } else {
        this.signUpError = "The given Passwords do not Match"
      }
    } else {
      this.signUpError = "Sorry that Username is Taken";
    }
  }

  switchModal() {
    this.viewSwitcher = !this.viewSwitcher;
    this.entryError = "";
    this.signUpError = "";
  }

}
