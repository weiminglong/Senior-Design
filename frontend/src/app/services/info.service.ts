import { Injectable, EventEmitter, Output } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InfoService {
  // TODO: change to subject or behavior subject to maintain value upon refresh
  private link: string;
  private timeFrames: string[][];
  private title: string;
  private query: string;

  constructor() { }

  sendLink(link: string){
    this.link = link;
  }

  sendTimeFrames(timeFrames: string[][]){
    this.timeFrames = timeFrames;
  }

  sendTitle(title: string){
    this.title = title;
  }

  getLink(){
    return this.link;
  }

  getTimeFrames(){
    return this.timeFrames;
  }

  getTitle(){
    return this.title;
  }

  setQuery(query: string){
    this.query = query;
  }

  getQuery(){
    return this.query;
  }

}
