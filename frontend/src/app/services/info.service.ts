import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InfoService {
  // TODO: change to subject or behavior subject to maintain value upon refresh
  private link: string;
  private timeFrames: string[][];

  constructor() { }

  sendLink(link: string){
    this.link = link;
  }

  sendTimeFrames(timeFrames: string[][]){
    this.timeFrames = timeFrames;
  }

  getLink(){
    return this.link;
  }

  getTimeFrames(){
    return this.timeFrames;
  }
}
