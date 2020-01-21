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

  setVideo(link: string){

    // example: adding child to video tag
    // var sourceTag = document.createElement('source');
    // sourceTag.setAttribute('src', this.videoURL);
    // sourceTag.setAttribute('type', 'video/mp4');
    // document.getElementById('video1').appendChild(sourceTag);

    // var video = document.getElementById('concept-video');
    // console.log(video);
    // console.log(video[0]);
    console.log("passing link: " + link);
    this.infoService.sendLink(link);
    
  }

  setTime(){
    (<HTMLMediaElement>document.getElementById('video1')).currentTime = 20;
  }

}
