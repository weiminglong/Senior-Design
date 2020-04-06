import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FlaskapiService } from '../services/flaskapi.service';
import { MatSnackBar } from '@angular/material';
import categoriesJson from '../../../../backend/src/categories.json';
import { FormControl } from '@angular/forms';
import { InfoService } from '../services/info.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {
  categories: String[] = categoriesJson['categories'];
  selectedCategory = new FormControl('');

  constructor(
    private flaskService: FlaskapiService,
    private snackBar: MatSnackBar,
    private infoService: InfoService,
    private router: Router) { }

  ngOnInit() {
  }

  onSelectedCategory(){
    console.log(this.selectedCategory.value);
    this.infoService.setCategoryFlag();
    this.infoService.setQuery(this.selectedCategory.value);
    this.router.navigate(['/list']);
  }
}
