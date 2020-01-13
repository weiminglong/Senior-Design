import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FlaskapiService } from '../services/flaskapi.service';

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

  videoFile = new FormControl('', Validators.required);
  videoTitle = new FormControl('', Validators.required);
  videoSubject = new FormControl('', Validators.required);
  newSubject = new FormControl('', Validators.required);

  constructor(private flaskService: FlaskapiService) { }

  ngOnInit() {
  }

  onVideoSelect(files: FileList){

    if (files.item(0) != null){
      this.videoToUpload = files.item(0);
      this.selectedVideo = files.item(0).name;
    } else {
      this.selectedVideo = "";
    }
  }

  onUpload(){
    // upload video...
    console.log("uploading: ");
    console.log(this.videoToUpload);

    this.flaskService.upload(this.videoToUpload).subscribe(
      resp => {
        console.log(resp); // print
      },
      err => {
        console.log("something went wrong:" + err);
      }
    )


  }

  resetForms(){
    this.videoSubject.reset();
    this.newSubject.reset();
  }

}
