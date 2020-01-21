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
        console.log(this.timeFrames);
      },
      err => {
        console.log("something went wrong:" + err);
      }
    )
  }

  onPlay(){
    
    this.flaskService.playVideo().subscribe(
      resp => {
        console.log("got video link");
        console.log(resp);
        this.videoURL = resp;
      },
      err => {
        console.log("something went wrong:" + err);
      }
    )
  }

  setVideo(index: number){

    // example: adding child to video tag
    // var sourceTag = document.createElement('source');
    // sourceTag.setAttribute('src', this.videoURL);
    // sourceTag.setAttribute('type', 'video/mp4');
    // document.getElementById('video1').appendChild(sourceTag);

    // var video = document.getElementById('concept-video');
    // console.log(video);
    // console.log(video[0]);
    
    console.log("passing index: " + index);
    console.log("passing url: " + this.videoNames[index]);
    console.log("passing time frames: " + this.timeFrames[index][0]);
    
    this.infoService.sendLink(this.videoNames[index]);
    this.infoService.sendTimeFrames(this.timeFrames[index]);
    
  }

  setTime(){
    (<HTMLMediaElement>document.getElementById('video1')).currentTime = 20;
  }

}
