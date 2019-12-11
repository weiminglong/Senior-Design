import { Component, OnInit } from '@angular/core';
import { FlaskapiService } from '../services/flaskapi.service';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {

  constructor(
    private flaskService: FlaskapiService,
    private snackBar: MatSnackBar) { }

  ngOnInit() {
  }

  onUpload(){
    this.flaskService.upload("upload video").subscribe(
      resp => {
        console.log(resp);
        this.snackBar.open(resp, 'Dismiss')

      },
      err => {
        console.log("something went wrong:" + err);
      }
    )
  }
}
