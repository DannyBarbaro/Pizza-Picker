import { Component, OnInit } from '@angular/core';
import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal';
import { LoginSignupComponent } from '../login-signup/login-signup.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  bsModalRef: BsModalRef;
  constructor(private modalService: BsModalService) {}

  openModal(hasAccount: boolean) {
    const initialState = { viewSwitcher: hasAccount };
    this.bsModalRef = this.modalService.show(LoginSignupComponent, { initialState });
  }
  ngOnInit() {
  }

}
