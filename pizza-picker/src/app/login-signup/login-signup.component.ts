import { Component, OnInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-login-signup',
  templateUrl: './login-signup.component.html',
  styleUrls: ['./login-signup.component.css']
})
export class LoginSignupComponent implements OnInit {

  viewSwitcher: boolean;
  entryError: String = "";
  signUpError: String = "";

  username: String = "";
  password: String = "";
  newUsername: String = "";
  newPassword: String = "";
  newPasswordConfirm: String = "";

  constructor(public bsModalRef: BsModalRef, private router: Router, private http: HttpClient) { }

  ngOnInit() {
  }

  signIn() {
    //http call for log in
    if (this.username.length !== 0 && this.password.length !== 0) {
      const headers = new HttpHeaders().set("user", <string>this.username).set("pass", <string>this.password);
      this.http.get<Boolean>('http://localhost:8080/auth', { headers })
        .subscribe((data: Boolean) => {
          if (data) {
            //route to the next page
            this.bsModalRef.hide();
            this.router.navigateByUrl('/userpage/' + this.username);
          } else {
            this.entryError = "Incorrect Username or Password";
          }
        });
    } else {
      this.entryError = "Please Fill in the Fields";
    }
  }

  signUp() {
    //http call to check if username is available
    let passwordMatch: boolean = this.newPassword === this.newPasswordConfirm;
    if (this.newUsername.length !== 0 && this.newPassword.length !== 0 && this.newPasswordConfirm.length !== 0) {
      if (this.newUsername.length <= 32) {
        this.http.get<Boolean>('http://localhost:8080/userExists/' + this.newUsername)
          .subscribe((data: Boolean) => {
            if (!data) {
              if (passwordMatch) {
                this.bsModalRef.hide();
                this.router.navigateByUrl('/userpage/' + this.newUsername);
              } else {
                this.signUpError = "The given Passwords do not Match"
              }
            } else {
              this.signUpError = "Sorry that Username is Taken";
            }
          });
        
      } else {
        this.signUpError = "Please limit username to 32 Characters"
      }
    } else {
      this.signUpError = "Please Fill in the Fields";
    }
  }

  switchModal() {
    this.viewSwitcher = !this.viewSwitcher;
    this.entryError = "";
    this.signUpError = "";
    this.username = "";
    this.password = "";
    this.newUsername = "";
    this.newPassword = "";
    this.newPasswordConfirm = "";
  }

}
