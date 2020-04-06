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
    private infoService: InfoService,
    private router: Router) {
      this.router.routeReuseStrategy.shouldReuseRoute = function(){
        return false;
      };
     }
 
  ngOnInit() {
  }

  onGo(){
    this.infoService.setQuery(this.searchTags.value);
    this.router.navigate(['/list']);
  }
}
