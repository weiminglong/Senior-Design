import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InfoService {
  private link: string;

  constructor() { }

  sendLink(link: string){
    this.link = link;
  }

  getLink(){
    return this.link;
  }
}
