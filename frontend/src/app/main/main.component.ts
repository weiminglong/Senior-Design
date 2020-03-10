import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FlaskapiService } from '../services/flaskapi.service';
import { InfoService } from '../services/info.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  @Output() sendQuery: EventEmitter<any> = new EventEmitter()
  searchTags = new FormControl('', Validators.required);
  videoNames: string[] = [];
  timeFrames: string[][][] = [];
  titles: string[] = [];
  names: string;
  videoURL: string;

  constructor(
    private flaskService: FlaskapiService,
    private infoService: InfoService,
    private router: Router) { }
 
  ngOnInit() {
  }

  onGo(){
    this.infoService.setQuery(this.searchTags.value);
    // console.log("set value: " + this.searchTags.value);
    this.router.navigate(['/list']);
  }

  setVideo(index: number){
    console.log("passing index: " + index);
    console.log("passing url: " + this.videoNames[index]);
    console.log("passing time frames: " + this.timeFrames[index][0]);
    console.log("passing title: " + this.titles[index]);
    
    this.infoService.sendLink(this.videoNames[index]);
    this.infoService.sendTimeFrames(this.timeFrames[index]);
    this.infoService.sendTitle(this.titles[index]);
  }

}
