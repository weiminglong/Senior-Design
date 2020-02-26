import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FlaskapiService } from '../services/flaskapi.service';
import { InfoService } from '../services/info.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  searchTags = new FormControl('', Validators.required);
  videoNames: string[] = [];
  timeFrames: string[][][] = [];
  titles: string[] = [];
  names: string;
  videoURL: string;

  constructor(
    private flaskService: FlaskapiService,
    private infoService: InfoService) { }
 
  ngOnInit() {
  }

  onGo(){
    //console.log(this.searchTags.value);

    this.flaskService.searchTags(this.searchTags.value).subscribe(
      resp => {
        console.log(resp); // print returned video name
        this.videoNames = resp[0];
        this.timeFrames = resp[1];
        this.titles = resp[2];
      },
      err => {
        console.log("something went wrong:" + err);
      }
    )
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
