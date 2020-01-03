import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  videoToUpload: File = null;
  categories: String[] = ["Math", "Physics", "Computer Science", "English", "History"];
  selectedVideo: string = "";

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

}
