import { Component, OnInit } from '@angular/core';
import { FlaskapiService } from '../services/flaskapi.service';
import { FormControl, Validators } from '@angular/forms';
import { InfoService } from '../services/info.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({ /** TODO: persistent search upon refresh */
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {
  searchTags = new FormControl('', Validators.required);
  videoNames: string[] = [];
  timeFrames: string[][][] = [];
  titles: string[] = [];

  constructor(private flaskService: FlaskapiService,
    private infoService: InfoService,
    private router: Router) {}

  ngOnInit() {
    if (this.infoService.getCategoryFlag() === 1 && this.infoService.getQuery() != undefined){
      this.infoService.unsetCategoryFlag();
      this.queryByCategory(this.infoService.getQuery());
    } else if (this.infoService.getQuery() != undefined){
      this.searchTags.setValue(this.infoService.getQuery());
      this.onGo();
    } else {
      this.router.navigate(['']);
    }
  }
  
  onGo(){
    console.log("onGo value: " + this.searchTags.value);

    this.flaskService.searchTags(this.searchTags.value).subscribe(
      resp => {
        console.log("resp:"); // print returned video name
        console.log(resp);

        this.videoNames = resp[0];
        this.timeFrames = resp[1];
        this.titles = resp[2];

        console.log(this.videoNames);
        console.log(this.timeFrames);
        console.log(this.titles);
        
      },
      err => {
        console.log("something went wrong:" + err);
      }
    )
  }
  
  queryByCategory(category: string){
    console.log('query by category method:');
    console.log(category);

    this.flaskService.searchVideosByCategory(category).subscribe(
      resp => {
        console.log(resp);

        this.videoNames = resp[0];
        this.timeFrames = resp[1];
        this.titles = resp[2];

        console.log(this.videoNames);
        console.log(this.timeFrames);
        console.log(this.titles);
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
