import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  videoToUpload: File = null;
  categories: String[] = ["Math", "Physics", "Computer Science", "English", "History"];
  selectedVideo: string = "";
  isChecked: boolean = false;

  videoTitle = new FormControl('', Validators.required);
  videoSubject = new FormControl('', Validators.required);
  newSubject = new FormControl('', Validators.required);

  constructor() { }

  ngOnInit() {
  }

  onVideoSelect(files: FileList){
    this.videoToUpload = files.item(0);
    this.selectedVideo = files.item(0).name;
  }

  onUpload(){
    // upload video...
  }

  resetForms(){
    this.videoSubject.reset();
    this.newSubject.reset();
  }

}
