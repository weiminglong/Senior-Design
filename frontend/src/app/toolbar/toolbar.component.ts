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
}
