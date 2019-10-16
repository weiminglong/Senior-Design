import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FlaskapiService } from '../services/flaskapi.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  searchTags = new FormControl('', Validators.required);
  videoNames: string[] = []
  names: string;

  constructor(private flaskService: FlaskapiService) { }
 
  ngOnInit() {
  }

  onGo(){
    //console.log(this.searchTags.value);

    this.flaskService.searchTags(this.searchTags.value).subscribe(
      resp => {
        console.log(resp); // print returned video name
        //this.videoNames = resp;
        this.names = resp;
      },
      err => {
        console.log("something went wrong:" + err);
      }
    )
  }

}
