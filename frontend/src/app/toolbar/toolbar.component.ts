import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FlaskapiService } from '../services/flaskapi.service';
import { MatSnackBar } from '@angular/material';
import categoriesJson from '../../../../backend/src/categories.json';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {
  categories: String[] = categoriesJson['categories'];
  constructor(
    private flaskService: FlaskapiService,
    private snackBar: MatSnackBar) { }

  ngOnInit() {
  }
}
