import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CarouselModule } from 'ngx-bootstrap/carousel';
import { PopoverModule } from 'ngx-bootstrap/popover';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginSignupComponent } from './login-signup/login-signup.component';
import { ModalModule } from 'ngx-bootstrap';
import { UserPageComponent } from './user-page/user-page.component';
import { HomeComponent } from './home/home.component';
import { UserHomeComponent } from './user-page/user-home/user-home.component';
import { UserFriendsComponent } from './user-page/user-friends/user-friends.component';
import { UserStatsComponent } from './user-page/user-stats/user-stats.component';
import {FormsModule} from '@angular/forms'
import { HttpClientModule } from '@angular/common/http';
import { ButtonsModule } from 'ngx-bootstrap/buttons';

@NgModule({
  declarations: [
    AppComponent,
    LoginSignupComponent,
    UserPageComponent,
    HomeComponent,
    UserHomeComponent,
    UserFriendsComponent,
    UserStatsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    ButtonsModule,
    CarouselModule.forRoot(),
    PopoverModule.forRoot(),
    ModalModule.forRoot(),
  ],
  providers: [],
  entryComponents:[LoginSignupComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }
