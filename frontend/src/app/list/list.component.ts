import { Component, OnInit } from '@angular/core';
import { FlaskapiService } from '../services/flaskapi.service';
import { FormControl, Validators } from '@angular/forms';
import { InfoService } from '../services/info.service';
import { Router } from '@angular/router';

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
    // this.infoService.getQueryString().subscribe(
    //   query => {
    //     console.log("this is the returned query: " + query);
    //     this.searchTags.setValue(query);
    //     console.log("this is the searchtags value: " + this.searchTags.value);

    //     if (query != undefined) {
    //       console.log("defined value: " + query);
    //       this.onGo();
    //     } else {
    //       console.log("undefined query value");
    //     }
    //   }
    // )

    if (this.infoService.getQuery() != undefined){
      this.searchTags.setValue(this.infoService.getQuery());
      this.onGo();
    } else {
      this.router.navigate(['']);
    }

    // this.searchTags.setValue("testing value");

    // console.log("searchtags value outside of subscription: " + this.searchTags.value);
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


}
